import os
import sys
import subprocess

logo = '''
     :+sMs.
  `:ddNMd-                         -o--`
 -sMMMMh:                          `+N+``
 yMMMMMs`     .....-/-...           `mNh/
 yMMMMMmh+-`:sdmmmmmmMmmmmddy+-``./ddNMMm
 STEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEGH
 STEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEG
  STEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEGHYST
  .STEGHYSTEGHYSTEGHYSTEGHYSTEGHYSTEGHYS.
 .omysmNNhy/+yNMMMMMMM-_-MNMMMMMMMMMNdNNy-
 /hMM:::::/hNMMMMMMM/      NMMMMMMM    MNh`
.hMMMMdhdMMMMMMMMMM|        MMMMMM      MM
:dMMMMMMMMMMMMMMMMM:    +   nMMMMM   +  MN
/dMMMMMMMMMMMMMMMMM/        :yMMMM:     MM.
:dMMMMMMMMMMMMMMMMMMn       oMMMMMMo/ dMNN/
:hMMMMMMMMMMMMMMMMMMM=MMsMsMMMMMMNNmyMMMMM/`
 sNMMMMMMMMMMMMMMMMMMMMMMMmmNMMMMMNhnMNM:o.
 :yMMMMMMMMMMMMMNho+sydNNNNNNNMMMmysso///
  /dMMMMMMMMMMMMMs-  ````````..``    //
   .oMMMMMMMMMMMMNs`               ./y:`
     +dNMMNMMMMMMMmy`          ``./ys.
      `/hMMMMMMMMMMMNo-``    `.+yy+-`
        `-/hmNMNMMMMMMmmddddhhy/-`
            `-+oooyMMMdsoo+/:.


 ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝

'''
#####################################################
#                                                   #
# SCRIPT FOR THE CONFIGURATION OF THE ENTIRE SYSTEM #
#    (sush as .vimrc, alacritty.yml, .bashrc)       #
#                                                   #
#####################################################

# user path:
USER_PATH = os.path.expanduser("~")

# source files:
SRC_DIR = USER_PATH + "/Documents/configs"

# .config dir
CNF_DIR = USER_PATH + "/.config"

# .local/share dir
LCL_SHARE_DIR = USER_PATH + "/.local/share"

# download path
temp_file = USER_PATH + "/temp"


def main():

    ########
    # MAIN #
    ########

    # update python first
    python_version = sys.version_info[0:3]
    if python_version < (3, 6, 0):
        sys.exit("==> this script require Python >= 3.6.0 \n"
                 "current python version %s" % sys.version)

    # NO ROOT!
    if os.geteuid() == 0:
        sys.exit("don't run this script as a root!")

    # fantastic title
    print(logo)                   # pacman steghy logo

    # network
    # resolv_dns()                  # test

    # update
    # system_apt_update()           # OK (always)

    # programs installation
    # apt_programs_installation()      # test
    # flatpak_programs_installation()  # test

    # delete old temp dir if it exists
    #  menage_temp_dir()             # ok

    # others
    # musikcube_installation()      # test

    # customization
    theme_installation()          # ok
    # font_installation()           # ok
    # icons_installation()          # ok

    # python libs
    # python_libs_installation()    # test

    # TEST
    # create_symlinks()             # symlinks creation..

    # configurations
    # vim_plugins_configuration()   # OK
    # tmux_plugins_configuration()  # OK

    # notification sound
    # notify()                      # OK


def create_symlinks():

    ############
    # SYMLINKS #
    ############

    # data files
    data = {

        # .vimrc
        USER_PATH+"/.vimrc": SRC_DIR+"/vim/.vimrc",

        # .tmux.conf
        USER_PATH+"/.tmux.conf": SRC_DIR+"/tmux/.tmux.conf",

        # alacritty.yml
        CNF_DIR+"/alacritty/alacritty.yml": SRC_DIR+"/alacritty/alacritty.yml",

        # neofetch/config.conf
        CNF_DIR+"/neofetch/config.conf": SRC_DIR+"/neofetch/config.conf",

        # musikcube/hotkeys
        CNF_DIR+"/musikcube/hotkeys": SRC_DIR+"/musikcube/hotkeys.json",

        # eclipse (?)
    }

    for k, v in data.items():

        # always overwrite old files
        if os.path.exists(k):
            subprocess.run(["rm", "--verbose", k])

        # alacritty, maybe neofetch
        parent_dir = os.path.dirname(k)
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        # symlink creation
        os.symlink(v, k)
        print("Creating symlink.[SOURCE]:%s, [DEST]:%s"
              % (v, k))


def resolv_dns():

    #######
    # DNS #
    #######

    target = "/etc/resolvconf/resolv.conf.d/head"
    source = SRC_DIR + "/dns/head"

    # remove old file
    subprocess.run(["sudo", "rm", "--verbose", target])

    # copy the new file
    subprocess.run(["sudo", "cp", source, os.path.dirname(target)])

    # update resolv.conf
    subprocess.run(["sudo", "rm", "--verbose", "/etc/resolv.conf"])

    # create the symlink
    subprocess.run(["sudo", "ln", "-s",
                    "../run/resolvconf/resolv.conf",
                    "/etc/resolv.conf"])
    # update
    subprocess.run(["sudo", "resolvconf", "-u"])


def notify():

    ################
    # NOTIFICATION #
    ################

    # sound to notify the termination of the configuration process
    from playsound import playsound
    playsound(SRC_DIR + "/notification/notification.wav")


def musikcube_installation():

    #############
    # MUSIKCUBE #
    #############

    # url
    musikcube_releases = "https://github.com/clangen/musikcube/releases"
    musikcube_0_98_0 = "/download/0.98.0/musikcube_standalone_0.98.0_amd64.deb"
    musikcube_url = musikcube_releases + musikcube_0_98_0

    # wget deb file
    code = subprocess.run(["wget", "-O", temp_file, musikcube_url]).returncode

    # something went wrong, don't proceed
    if code:
        return

    # installation
    subprocess.run(["sudo", "dpkg", "-i", temp_file])

    # remove temporary file
    subprocess.run(["rm", "-v", temp_file])


def font_installation():

    ########
    # FONT #
    ########

    # url
    hack_releases_url = "https://github.com/ryanoasis/nerd-fonts/releases"
    version = "/download/v2.1.0/Hack.zip"
    hack_font_url = hack_releases_url + version

    # wget files
    code = subprocess.run(["wget", "-O", temp_file, hack_font_url]).returncode

    # something went wrong, don't proceed
    if code:
        return

    # fonts dir
    fonts_dir = USER_PATH + "/.fonts"

    # if it doesn't exists, create.
    if os.path.exists(fonts_dir):
        subprocess.run(["rm", "-rfv", fonts_dir])
    os.mkdir(fonts_dir)

    # unzip the font
    subprocess.run(["unzip", temp_file, "-d", fonts_dir +
                    "/hack-nerd-font"])

    # refresh the fc-cache
    subprocess.run(["fc-cache", "-fv"])

    # removing temporary files
    subprocess.run(["rm", "rfv", temp_file])


def menage_temp_dir():

    # check temp
    if os.path.exists(temp_file):

        # delete it
        subprocess.run(["rm", "-rfv", temp_file])


def theme_installation():

    #########
    # THEME #
    #########

    # url
    mojave_git_url = "https://github.com/vinceliuice/Mojave-gtk-theme.git"

    # clone the repo
    subprocess.run(["git", "clone", mojave_git_url, temp_file])

    # themes path
    themes_path = USER_PATH + "/.themes"

    # check if already exists
    if os.path.exists(themes_path):
        subprocess.run(["rm", "-rfv", themes_path])
    os.mkdir(themes_path)

    # execute the script
    subprocess.run(["bash", temp_file + "/install.sh",
                    "-d", themes_path,  # destination
                    "-n", "mojave-dark-solid",     # theme name
                    "-c", "dark",                  # color
                    "-o", "solid",                 # opacity
                    "-a", "standard",              # title-button
                    "-s", "small",                 # button-size
                    "-t", "grey",                  # other colors
                    "-i", "arch"])                 # activities logo

    # removing temporary files
    subprocess.run(["rm", "-rfv", temp_file])


def icons_installation():

    #########
    # ICONS #
    #########

    # url
    zafiro_git_url = "https://github.com/zayronxio/Zafiro-icons.git"

    # clone the repo
    code = subprocess.run(["git", "clone",
                           zafiro_git_url, temp_file]).returncode

    # something went wrong, don't proceed
    if code:
        return

    # default user icons path
    icons_path = LCL_SHARE_DIR + "/icons"

    # if exists, delete it
    if os.path.exists(icons_path):
        subprocess.run(["rm", "-rfv", icons_path])
    os.mkdir(icons_path)

    # execute the script
    subprocess.run(["bash", temp_file + "/Install-Zafiro-Icons.sh"])

    # deleting temporary files
    subprocess.run(["rm", "-rfv", temp_file])


def system_apt_update():

    #################
    # SYSTEM UPDATE #
    #################

    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "upgrade"])


def python_libs_installation():

    ############################
    # PYTHON LIBS INSTALLATION #
    ############################

    # some python lib
    subprocess.run(["pip", "install", "pyfiglet",
                    "ddt", "flake8", "pillow",
                    "pypi-json", "requests",
                    "playsound"])


def vim_plugins_configuration():

    ##############################
    # VIM PLUGINS CONFIGURATION  #
    ##############################

    # default vundle dir
    vundle_path = "/.vim/bundle/Vundle.vim"

    # remove old vundle dir if exists
    if os.path.exists(USER_PATH + vundle_path):
        subprocess.run(["rm", "-rfv", USER_PATH + vundle_path])

    # clone vundle
    git_vundle_code = \
        subprocess.run(["git", "clone",
                        "https://github.com/VundleVim/Vundle.vim.git",
                        USER_PATH + vundle_path]).returncode

    # plugins installation
    if not git_vundle_code:
        vim_plugins_code = subprocess.run(["vim", "-c",
                                           "PluginInstall",
                                           "+qall"]).returncode
        # ycm installation
        if not vim_plugins_code:
            subprocess.run([USER_PATH + "/.vim/bundle/YouCompleteMe/" +
                            "install.py", "--all"]).returncode


def tmux_plugins_configuration():

    ##############################
    # TMUX PLUGINS CONFIGURATION #
    ##############################

    # default tmux dir
    tpm_path = "/.tmux/plugins/tpm"

    # remove old tpm dir if exists
    if os.path.exists(USER_PATH + tpm_path):
        subprocess.run(["rm", "-rfv", USER_PATH + tpm_path])

    # clone tpm
    git_tpm_code = subprocess.run(["git", "clone",
                                   "https://github.com/" +
                                   "tmux-plugins/tpm",
                                   USER_PATH + tpm_path]).returncode
    # refresh tmux envirnment
    if not git_tpm_code:
        tmux_refr_env_code = subprocess.run(["tmux", "source",
                                             USER_PATH +
                                             "/.tmux.conf"]).returncode
        # plugins installation
        if not tmux_refr_env_code:
            subprocess.run(["bash", USER_PATH + "/.tmux/plugins/" +
                            "tpm/scripts/" + "install_" + "plugins.sh"])


def flatpak_configuration():

    #########################
    # FLATPAK CONFIGURATION #
    #########################

    subprocess.run("flatpak remote-add --user --if-not-exists"
                   "flathub https://flathub.org/repo/flathub."
                   "flatpakrepo", shell=True)


def flatpak_programs_installation():

    #########################
    # PROGRAMS FROM FLATPAK #
    #########################

    # flathub repository
    flatpak_configuration()

    # programs installation
    subprocess.run(["flatpak", "install", "flathub",
                    "org.eclipse.Java"])


def apt_programs_installation():

    #####################
    # PROGRAMS FROM APT #
    #####################

    subprocess.run(["sudo", "apt", "install",
                    "alacritty",             # terminal
                    "build-essential",       # ycm dependence
                    "calcurse",              # terminal calendar
                    "calibre",               # books manager
                    "cava",                  # music visualizer
                    "cmake",                 # required
                    "cmatrix",               # fun
                    "curl",                  # required
                    "default-jdk",           # ycm dependence
                    "discord",               # chat
                    "dpkg",                  # required
                    "flatpak",               # other pkgm
                    "git",                   # required
                    "gnome-tweaks",          # customization
                    "golang",                # ycm dependence
                    "google-chrome-stable",  # browser
                    "htop",                  # process viewer
                    "inkscape",              # images
                    "mono-complete",         # ycm dependence
                    "neofetch",              # the best
                    "nodejs",                # ycm dependence
                    "npm",                   # ycm dependence
                    "python3-dev",           # ycm dependence
                    "python3-pip",           # python pkgm
                    "telegram-desktop",      # chats
                    "tmux",                  # terminal mux
                    "vim",                   # text editor
                    "vim-nox",               # ycm dependence
                    "vlc",                   # video player
                    "wget"])                 # required


# call
if __name__ == "__main__":
    main()
