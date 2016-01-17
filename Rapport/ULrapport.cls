%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%                                                             %%%%%%%%%%%%%
%%%%%%%%%%%%%   Classe de document "ULrapport"                            %%%%%%%%%%%%%
%%%%%%%%%%%%%   par Pierre Tremblay, Universite Laval                     %%%%%%%%%%%%%
%%%%%%%%%%%%%   2008/03/28 - version 1.1g                                 %%%%%%%%%%%%%
%%%%%%%%%%%%%                                                             %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%--------------------------------------------------------------------------------------
%----------------------------------- identification -----------------------------------
%--------------------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ULrapport}%
              [2008/03/28 v1.1g Classe de rapport technique - Universite Laval]
%--------------------------------------------------------------------------------------
%------------------------------------ initial code ------------------------------------
%--------------------------------------------------------------------------------------
%**************************************************************************************
% Flags logiques permettant l'insertion des listes des figures et des tableaux
%
\RequirePackage{ifthen}
\newboolean{InsererListeDesFigures}
\newboolean{InsererListeDesTableaux}
%**************************************************************************************
%--------------------------------------------------------------------------------------
%------------------------------- declaration of options -------------------------------
%--------------------------------------------------------------------------------------
\DeclareOption{ULlof}{\setboolean{InsererListeDesFigures}{true}}
\DeclareOption{ULlot}{\setboolean{InsererListeDesTableaux}{true}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
%--------------------------------------------------------------------------------------
%-------------------------------- execution of options --------------------------------
%--------------------------------------------------------------------------------------
\ProcessOptions \relax
%--------------------------------------------------------------------------------------
%----------------------------------- package loading ----------------------------------
%--------------------------------------------------------------------------------------
\LoadClass{report}
%
\RequirePackage{geometry}
\RequirePackage{lmodern}
\RequirePackage[T1]{fontenc}
\RequirePackage[USenglish,french]{babel}
\RequirePackage{caption}
\RequirePackage{textcomp}        % pour \textcelsius, \textmu, \textohm,
                                 % \textdegree (\degres de Babel)
\RequirePackage{array}
\RequirePackage{amstext}         % pour \text
\RequirePackage{tabularx}
\RequirePackage{colortbl}
\RequirePackage{longtable}
\RequirePackage{graphicx}
\RequirePackage{rotating}
% \RequirePackage{mathabx}         % pour \second (peut etre remplace par "\prime\prime")
% \RequirePackage{color}
\RequirePackage[hyphens]{url}
\RequirePackage{hyperref}
%--------------------------------------------------------------------------------------
%-------------------------------------- main code -------------------------------------
%--------------------------------------------------------------------------------------
%**************************************************************************************
% Definitions des parametres du package hyperref
%
\hypersetup{plainpages=false,%
            breaklinks=false,%
            colorlinks=true}
%**************************************************************************************
%**************************************************************************************
% Definitions des dimensions de la page (package geometry)
%
\geometry{letterpaper,%
          centering,%
          hmargin={2.5cm,2.5cm},%
          vmargin={2.5cm,2.5cm},%
          heightrounded,%
          includehead}
%**************************************************************************************
%**************************************************************************************
% Utilisation du package "caption" pour
%    - redefinit le caractere de separation dans les legendes comme "babel" le definit,
%      car "caption" (ou "float", le cas echeant) le redefinit comme ":"
%    - uniformise les legendes entre table, longtable et supertabular
%    - specifie que la legende des tableaux sera placee en haut,
%      donc intervertit les dimensions d'espacements (avant et apres la legende)
%
\DeclareCaptionLabelSeparator{as-Babel-french}{\space\textendash\space}
\captionsetup{margin=0.1\textwidth,labelsep=as-Babel-french}
\captionsetup[table]{position=top}
%**************************************************************************************
%**************************************************************************************
% Redefinition de l'environnement "thebibliography" afin que son existence soit
% mentionnee a la table des matieres
%
\newenvironment{thebibliographyUL}[1]%
               {\clearpage%
                \begin{thebibliography}{#1}%
                \addcontentsline{toc}{chapter}{\bibname}%
                \raggedright%
               }%
               {\end{thebibliography}}
%**************************************************************************************
%**************************************************************************************
% En-tete et bas de page par defaut
%
\pagestyle{headings}
%**************************************************************************************
%**************************************************************************************
% Definitions pour l'inclusion de graphiques
%    - des repertoires par defaut
%    - des extensions supportees
%
\graphicspath{{./pdf/}{./pic/}}
\DeclareGraphicsExtensions{.jpg,.png}
%**************************************************************************************
%**************************************************************************************
% Definitions de la page titre
%
\renewcommand{\maketitle}{%
   \thispagestyle{empty}%
   \pagenumbering{roman}%
   \begin{titlepage}%
      \setcounter{page}{999}%                      % associe le numero "0" a la page titre
      \begin{flushleft}
         \includegraphics[width=12em]{UL_P.pdf}
      \end{flushleft}\par
      \vspace*{\stretch{2}}
      \begin{center}
         \parbox{\textwidth}{\centering\Large\bfseries \theTitreProjet}         \\[5ex]
         \parbox{\textwidth}{\centering\large\bfseries \theTitreRapport}        \\
         \vspace*{\stretch{2}}
         pr\'{e}sent\'{e} \`{a}                    \\[1ex]
         \textbf{\theDestinataire}                 \\
         \vspace*{\stretch{1}}
         par                                       \\[1ex]
         {\large \'{E}quipe \theNumeroEquipe\
                 --- \theNomEquipe}                \\[1ex]
      \end{center}
      \renewcommand{\arraystretch}{1.5}            % plus d'espace pour les signatures
      \begin{tabularx}{\textwidth}%
         {|l|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}
         \hline
         \multicolumn{1}{|c|}{\emph{matricule}}
         & \multicolumn{1}{c|}{\emph{nom}}
         & \multicolumn{1}{c|}{\emph{signature}}
         \\\hline
         \theTableauMembres
      \end{tabularx}\par
      \vspace*{\stretch{1}}
      \begin{center}
         {\large Universit\'{e} Laval}             \\
         \theDateRemise
      \end{center}
   \end{titlepage}%
   \clearpage%
   \let\maketitle\relax%
}
%**************************************************************************************
%**************************************************************************************
% Definitions des fonctions permettant de definir les parametres de la page titre
%
%\newcommand{\theTitreProjet}{\foreignlanguage{french}{Titre du projet}}                  % Titre du projet
%\newcommand{\TitreProjet}[1]{\renewcommand{\theTitreProjet}{\foreignlanguage{french}{#1}}}           % Titre du projet
\def\TitreProjet#1{\def\theTitreProjet{#1}}           % Titre du projet
\def\TitreRapport#1{\def\theTitreRapport{#1}}         % Titre du rapport
\def\Destinataire#1{\def\theDestinataire{#1}}         % Nom(s) du destinataire
\def\NumeroEquipe#1{\def\theNumeroEquipe{#1}}         % Numero de l'equipe
\def\NomEquipe#1{\def\theNomEquipe{#1}}               % Nom de l'equipe
\def\TableauMembres#1{\def\theTableauMembres{#1}}     % Tableau des membres de l'equipe
\def\DateRemise#1{\def\theDateRemise{#1}}             % Date de remise
\def\HistoriqueVersions#1%
   {\def\theHistoriqueVersions{#1}}                   % Historique des versions
%**************************************************************************************
%**************************************************************************************
% Definitions des parametres par defaut de la page titre
%
\def\theTitreProjet{Titre du projet}                  % Titre du projet
\def\theTitreRapport{Titre du rapport}                % Titre du rapport
\def\theDestinataire{Destinataire}                    % Nom(s) du destinataire
\def\theNumeroEquipe{XX}                              % Numero de l'equipe
\def\theNomEquipe{Nom de l'\'{e}quipe}                % Nom de l'equipe
\def\theTableauMembres{matricule & nom & \\\hline}    % Tableau des membres de l'equipe
\def\theDateRemise{Date de remise}                    % Date de remise
\def\theHistoriqueVersions%
   {version & date & description \\\hline}            % Historique des versions
%**************************************************************************************
%**************************************************************************************
% Definition du niveau hierarchique maximum couvert par la table des matieres
%
\setcounter{tocdepth}{3}            % default = 2
%**************************************************************************************
%**************************************************************************************
% Definition du niveau hierarchique maximum ayant une numerotation
%
\setcounter{secnumdepth}{3}         % default = 2
%**************************************************************************************
%**************************************************************************************
% Definitions des parametres du package hyperref - details propres au rapport
%
\AtBeginDocument{%
   \hypersetup{pdftitle={\theTitreProjet},%
               pdfsubject={\theTitreRapport},%
               pdfauthor={\'{E}quipe \theNumeroEquipe\ - \theNomEquipe}}%
}
%**************************************************************************************
%**************************************************************************************
% Selection de la langue "babel" par defaut
%
\AtBeginDocument{%
   \selectlanguage{french}%
}
%**************************************************************************************
%**************************************************************************************
% Changement des mots utilises par "babel" par defaut (figure et table)
%
\AtBeginDocument{%
   \renewcommand{\figurename}{\textsc{Figure}}%
   \renewcommand{\tablename}{\textsc{Tableau}}%
}
%**************************************************************************************
%**************************************************************************************
% Generation de la page titre
%
\AtBeginDocument{%
   \maketitle
}
%**************************************************************************************
%**************************************************************************************
% Generation de la page d'historique des versions ("Document Change Record")
%
\AtBeginDocument{%
   \thispagestyle{empty}%
   \setcounter{page}{0}%
   \noindent%
   \begin{tabularx}{\textwidth}%
      {|c|l|>{\raggedright\arraybackslash}X|}
      \hline\hline
      \multicolumn{3}{|c|}{\large\rule[-2.25ex]{0ex}{6ex}%
                           \textsf{Historique des versions}}
      \\\hline
      \multicolumn{1}{|c|}{\emph{version}}
      & \multicolumn{1}{c|}{\emph{date}}
      & \multicolumn{1}{c|}{\emph{description}}
      \\\hline
      \theHistoriqueVersions\hline
   \end{tabularx}\par
   \clearpage
}
%**************************************************************************************

%**************************************************************************************
% Generation de la table des matieres, de la liste des figures, de la liste des tableaux
%
\AtBeginDocument{%
   \tableofcontents
   \ifthenelse{\boolean{InsererListeDesFigures}}%
              {\clearpage%
               \listoffigures%
               \addcontentsline{toc}{chapter}{\listfigurename}}{}
   \ifthenelse{\boolean{InsererListeDesTableaux}}%
              {\clearpage%
               \listoftables%
               \addcontentsline{toc}{chapter}{\listtablename}}{}
}
%**************************************************************************************
%**************************************************************************************
% Reinitialisation du compteur "page" (valeur et style)
%
\AtBeginDocument{%
   \cleardoublepage%
   \setcounter{page}{1}%
   \pagenumbering{arabic}%
}
%**************************************************************************************
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%                                                             %%%%%%%%%%%%%
%%%%%%%%%%%%%   Historique des versions                                   %%%%%%%%%%%%%
%%%%%%%%%%%%%                                                             %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%   2008/03/28 - version 1.1g                                 %%%%%%%%%%%%%
% Repositionnement de "\addcontentsline" pour assurer un hyperlien correct (3 fois)
% par Jean-Dominic Laroche (GLO)
% Ajout du package "url" avec option "hyphens" pour faciliter la cesure des urls
% Ajout de la commande "\raggedright" a la bibliographie pour faciliter la mise en page
% et eliminer les nombreux "underfull" autrement generes
%
%%%%%%%%%%%%%   2008/02/08 - version 1.1f                                 %%%%%%%%%%%%%
% Utilisation de \parbox pour presenter les titres longs avec un espacement correct
%
%%%%%%%%%%%%%   2007/12/02 - version 1.1e                                 %%%%%%%%%%%%%
% Ajout de la bibliographie et des listes a la table des matieres par l'environnement
% "thebibliographyUL"
% Ajout de l'historique des versions
%
%%%%%%%%%%%%%   2007/05/05 - version 1.1d                                 %%%%%%%%%%%%%
% Ajout des compteurs "tocdepth" et "secnumdepth" pour la numerotation des sections
% Ajout des flags logiques pour l'insertion facultative des listes (figures, tableaux)
%
%%%%%%%%%%%%%   2007/04/12 - version 1.1c                                 %%%%%%%%%%%%%
% Changement de "\theEquipe" pour "\theNumeroEquipe" et "\theNomEquipe"
% Ajout des flags logiques pour l'insertion facultative des listes (figures, tableaux)
%
%%%%%%%%%%%%%   2007/02/01 - version 1.1b                                 %%%%%%%%%%%%%
% Retrait de l'option d'hyperref "pdfpagelables=true", car deja par defaut
%
%%%%%%%%%%%%%   2007/01/17 - version 1.1a                                 %%%%%%%%%%%%%
% Ajout de "\renewcommand{\arraystretch}{1.5}" a la page titre
%
%%%%%%%%%%%%%   2007/01/16 - version 1.1                                  %%%%%%%%%%%%%
% Mise a jour complete
%
%%%%%%%%%%%%%   2006/03/01 - version 1.0                                  %%%%%%%%%%%%%
% Creation
%



% A FAIRE
% - ajouter \subsubsubsection{}
% - forcer 12pt
% - corriger selon les dernieres modifications de babel (mars 2008)

