# autoChangeCheck_F-KDE

This tool automates the check for changes related to the package maintenance of KDE packages within Fedora: it identifies KDE-sided and Fedora-sided changes. It's intended to make the packager aware of changes that could be relevant for their packaging pipeline and that justify a review of the pipeline: it's intentional fragile and quickly informs the packager that they have to review something (it's not proven everything is relevant to packaging, but the review/decision is left to the packager). Some changes just change variables, some raise exceptions: both is intended in this tool, and both will be considered in the output to the log file. It aims to tackle the type of case in which a packager has a broken pipeline for a year or two without noticing.

This tool does NOT do anything but checking if changes have occurred in either distgit (Fedora) or sourcegit (invent.KDE) or download.kde.org/stable/release-service, and if any of that has been changed, inform the user. 

## Presumptions of this experimental tool!

The folder names of a given package within "distgit/" and within "sourcegit/" must be **equal** (e.g., `kate` in both cases). Do **not** run this as root. In "distgit/", only **commits** in the current branch (must be set to "**rawhide**" before use!) are considered to be changes. In "sourcegit/", only new **references** are considered to be changes. At this time, this tool is intended only for cases in which "%{stable_kf6}" is "**stable**". Internet connection is assumed to be available. All folders in "distgit/" and "sourcegit/" are assumed to be git repos. Python3 and the necessary modules are assumed to be installed, but should be installed by default on Fedora anyway (as of F44). The tool assumes the system to be **trusted**, and that all changes that are packaging-relevant are directly or indirectly triggering "distgit/" or "sourcegit/" changes.

The repos in "distgit/" and "sourcegit/" are **not** suitable to work in: after creating the clones, only this tool should modify any content (exception in "distgit/": if "rawhide" is for whatever reason **not** the default branch, make it default).

This tool is experimental and was originally intended only to temporarily fill a gap in my workflow. The tool has little fault tolerance and presumes several conditions that must be ensured by the environment in which this tool is deployed. The tool is intended to fit my workflow and is intended to fulfill only a very specific and limited task. Be careful with it (and know the implications of the presumptions). This is **not** an official KDE or Fedora tool.

Maybe I add later a partially-redundant check for package-related changes in https://download.kde.org/stable/release-service/. Maybe I will improve the tool over time and replace some presumptions with appropriate checks and better exception handling, but maybe I use this tool only as short-term mitigation.


## How to use this tool:

It is necessary to have a working directory that contains the folders "distgit/", "sourcegit/" and the file "kdedownload_previous-versions". The file "kdedownload_previous-versions" can be automatically created by the tool, but the folders "distgit/" and "sourcegit/" - including their contained git repositories - must be **created before** this tool is started the first time!

In order to make the tool work, at least one **package has to be added**: adding packages works by cloning the distgit repo into the folder "distgit/" and cloning the KDE source git into the folder "sourcegit/". E.g., `/working/dir/sourcegit/kate` and `/working/dir/distgit/kate`.

Please carefully read the above presumptions that must be met before running this tool for the first time!

Then, you can run the tool with the working directory:
`python3 autoChangeCheck_F-KDE.py /working/dir/`

The path must be **absolute**: it has to begin with `/`. `~` is **not** yet supported!

The output file will be on the Desktop of the user who runs the tool. The file will be not deleted but appended. It's the user's choice if they want to delete it once it has been processed.

## Improvements, ideas

If you have improvements or ideas, feel free to file a PR or open a ticket.
