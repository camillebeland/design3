import serial
import serial.tools.list_ports as lp
from configuration import configuration
from maestroControl.prehenseur_rotation_control import PrehenseurRotationControl
from utils.assemblers.position_assembler import PositionAssembler
from robot import robot_web_controller
from robot.action_machine import ActionMachine
from robot.actions.discover_manchester_code import DiscoverManchesterCodeAction
from robot.actions.drop_down_treasure import DropDownTreasure
from robot.actions.end_sequence import EndSequenceAction
from robot.actions.find_best_treasure import FindBestTreasureAction
from robot.actions.find_island import FindIslandAction
from robot.actions.find_island_clue import FindIslandClue
from robot.actions.move_to_charge_station import MoveToChargeStationAction
from robot.actions.move_to_target_island import MoveToTargetIslandAction
from robot.actions.move_to_treasure import MoveToTreasureAction
from robot.actions.pick_up_treasure import PickUpTreasureAction
from robot.actions.recharge import RechargeAction
from robot.battery import Battery
from robot.context import Context
from robot.magnet import Magnet
from robot.manchester_antenna_usb_controller import ManchesterAntennaUsbController
from robot.map import Map
from robot.movement import Movement
from robot.robot import Robot
from robot.robot_service import RobotService
from robot.simulation.battery_simulation import BatterySimulation
from robot.simulation.error_simulation import NoisyWheels
from robot.simulation.magnet_simulation import MagnetSimulation
from robot.simulation.manchester_antenna_simulation import ManchesterAntennaSimulation
from robot.simulation.robot_service_simulation import RobotServiceSimulation
from robot.simulation.simulation_map import SimulationMap
from robot.vision_refresher import VisionRefresher
from robot.wheels_correction_layer import WheelsCorrectionLayer
from robot.wheels_usb_commands import WheelsUsbCommands
from robot.wheels_usb_controller import WheelsUsbController
from robot.worldmap_service import WorldmapService
from robot.treasure_easiest_path import TreasureEasiestPath


if __name__ == '__main__':
    config = configuration.get_config()

    host = config.get('robot', 'host')
    port = config.getint('robot', 'port')
    wheels_config = config.get('robot', 'wheels')
    base_station_host = config.get('baseapp', 'host')
    base_station_port = config.get('baseapp', 'port')
    base_station_camera = config.get('baseapp', 'camera')
    base_station_address = "http://" + base_station_host + ":" + base_station_port
    island_server_address = config.get('island_server', 'host')
    loop_time = config.getfloat('robot', 'loop-time')
    min_distance_to_destination = config.getfloat('robot', 'min-distance-to-destination')

    robot_service = RobotService(island_server_address)
    world_map_service = WorldmapService(base_station_host,base_station_port)
    if wheels_config == "simulation":
        world_map = SimulationMap(1600, 1200, world_map_service)
        try:
            refresh_time = config.getint('robot', 'wheels-refresh-time')
        except:
            print("Warning : wheels-refresh-time not specified, setting 10")
            refresh_time = 10

        try:
            wheels_velocity = config.getint('robot', 'wheels-velocity')
        except:
            print("Warning : wheels-velocity not specified, setting 5")
            wheels_velocity = 5

        try:
            noise = config.getint('robot', 'simulation-noise')
        except:
            print("Warning : noise not specified, setting 0")
            noise = 0

        wheels = NoisyWheels(world_map, refresh_time=refresh_time, wheels_velocity=wheels_velocity, noise=noise)
        corrected_wheels = WheelsCorrectionLayer(wheels, 1.0)
        manchester_antenna = ManchesterAntennaSimulation()
        battery = BatterySimulation()
        magnet = MagnetSimulation()
        robot_service = RobotServiceSimulation()

    elif wheels_config == "usb-arduino":
        world_map = Map(world_map_service)

        arduino_pid = config.getint('robot', 'arduino-pid')
        arduino_vid = config.getint('robot', 'arduino-vid')
        polulu_pid = config.getint('robot', 'polulu-pid')
        polulu_vid = config.getint('robot', 'polulu-vid')
        arduino_baudrate = config.getint('robot', 'arduino-baudrate')
        ports = lp.comports()
        arduino_port = list(filter(lambda port: port.pid == arduino_pid and port.vid == arduino_vid, ports))
        polulu_port = list(filter(lambda port: port.pid == polulu_pid and port.vid == polulu_vid, ports))
        assert(len(list(arduino_port)) != 0)
        assert(len(list(polulu_port)) != 0)
        real_polulu_port = min(map(lambda x: x.device, polulu_port))
        arduino_serial_port = serial.Serial(port=arduino_port[0].device, baudrate=arduino_baudrate, timeout=1)
        wheels = WheelsUsbController(arduino_serial_port, WheelsUsbCommands())

        corrected_wheels = WheelsCorrectionLayer(wheels, 1.0)
        manchester_antenna = ManchesterAntennaUsbController(arduino_serial_port)
        battery = Battery(arduino_serial_port)
        polulu_port_serial = serial.Serial(port=real_polulu_port, timeout=1)
        prehenseur = PrehenseurRotationControl(polulu_port_serial)
        magnet = Magnet(arduino_serial_port, prehenseur)
        robot_service = RobotService(island_server_address)

    movement = Movement(compute=None, sense=world_map, control=wheels, loop_time=loop_time,
                        min_distance_to_destination=min_distance_to_destination)
    robot = Robot(wheels=corrected_wheels, world_map=world_map, pathfinder=None, manchester_antenna=manchester_antenna,
                  movement=movement, battery=battery, magnet=magnet)

    treasure_easiest_path = TreasureEasiestPath()
    vision_refresher = VisionRefresher(robot, corrected_wheels, base_station_host, base_station_port, treasure_easiest_path)

    action_machine = ActionMachine()

    context = Context(robot, robot_service, world_map, None, action_machine, treasure_easiest_path)

    move_to_charge_station = MoveToChargeStationAction(context, 'move_to_charge_station_done')
    pick_up_treasure = PickUpTreasureAction(context, 'pick_up_treasure_done')
    drop_down_treasure = DropDownTreasure(context, 'drop_down_treasure_done')
    discover_manchester_code = DiscoverManchesterCodeAction(context, 'discover_manchester_code_done')
    find_island_clue = FindIslandClue(context, 'find_island_clue_done')
    recharge = RechargeAction(context, 'recharge_done')
    find_best_treasure = FindBestTreasureAction(context, 'find_best_treasure_done')
    find_island = FindIslandAction(context, 'find_island_done')
    move_to_target_island = MoveToTargetIslandAction(context, 'move_to_target_island_done')
    end_action = EndSequenceAction(context, None)
    move_to_treasure = MoveToTreasureAction(context, 'move_to_treasure_done')


    action_machine.register('move_to_charge_station', move_to_charge_station)
    action_machine.register('discover_manchester_code', discover_manchester_code)
    action_machine.register('pick_up_treasure', pick_up_treasure)
    action_machine.register('end_action', end_action)
    action_machine.register('drop_down_treasure', drop_down_treasure)
    action_machine.register('find_island_clue', find_island_clue)
    action_machine.register('recharge', recharge)
    action_machine.register('move_to_target_island', move_to_target_island)
    action_machine.register('move_to_treasure', move_to_treasure)
    action_machine.register('find_island', find_island)
    action_machine.register('find_best_treasure', find_best_treasure)


    action_machine.bind('move_to_charge_station', 'move_to_charge_station')
    action_machine.bind('find_island', 'find_island')
    action_machine.bind('move_to_treasure', 'move_to_treasure')
    action_machine.bind('move_to_target_island', 'move_to_target_island')
    action_machine.bind('find_best_treasure', 'find_best_treasure')
    action_machine.bind('pick_up_treasure', 'pick_up_treasure')
    action_machine.bind('drop_down_treasure', 'drop_down_treasure')
    action_machine.bind("read_manchester", "discover_manchester_code")
    action_machine.bind('find_island_clue', 'find_island_clue')
    action_machine.bind("recharge", "recharge")


    action_machine.bind('start', 'move_to_charge_station')
    action_machine.bind('move_to_charge_station_done', 'recharge')
    action_machine.bind('recharge_done', 'discover_manchester_code')
    action_machine.bind('discover_manchester_code_done', 'find_island_clue')
    action_machine.bind('find_island_clue_done', 'find_island')
    action_machine.bind('find_island_done', 'find_best_treasure')
    action_machine.bind('find_best_treasure_done', 'move_to_treasure')
    action_machine.bind('move_to_treasure_done', 'pick_up_treasure')
    action_machine.bind('pick_up_treasure_done', 'move_to_target_island')
    action_machine.bind('move_to_target_island_done', 'drop_down_treasure')
    action_machine.bind('drop_down_treasure_done', 'end_action')


    robot_web_controller.inject(robot, vision_refresher, robot_service, action_machine, PositionAssembler())
    robot_web_controller.run(host, port)
