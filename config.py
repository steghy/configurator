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
LCL_DIR = USER_PATH + "/.local/share"


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
    resolv_dns()                  # dns problem resolution

    # update
    system_apt_update()           # update

    # programs installation
    apt_programs_installation()      # programs installation (apt)
    flatpak_programs_installation()  # programs installation (flatpak)

    # others
    musikcube_installation()      # Musikcube installation..

    # delete old temp dir if it exists
    menage_temp_dir()

    # customization
    theme_installation()          # Mojave dark installation..
    font_installation()           # Fira code font installation..
    icons_installation()          # Zafiro icons installation..

    # python libs
    python_libs_installation()    # pip install..

    # symlinks
    create_symlinks()             # symlinks creation..

    # configurations
    vim_plugins_configuration()   # vim configuration..
    tmux_plugins_configuration()  # tmux configuration..

    # notification sound
    notify()                      # notification sound


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

    # path
    download_path = USER_PATH + "/temp"

    # wget deb file
    subprocess.run(["wget", "-O", download_path, musikcube_url])

    # installation
    subprocess.run(["sudo", "dpkg", "-i", download_path])

    # remove temporary file
    subprocess.run(["rm", "--verbose", download_path])


def font_installation():

    ########
    # FONT #
    ########

    # url
    hack_releases_url = "https://github.com/ryanoasis/nerd-fonts/releases"
    version = "/download/v2.1.0/Hack.zip"
    hack_font_url = hack_releases_url + version

    # download path
    download_path = USER_PATH + "/temp"

    # wget files
    subprocess.run(["wget", "-O", download_path, hack_font_url])

    # fonts dir
    fonts_dir = USER_PATH + "/.fonts"

    # if it doesn't exists, create.
    if not os.path.exists(fonts_dir):
        os.mkdir(fonts_dir)

    # unzip the font
    subprocess.run(["unzip", download_path, "-d", fonts_dir + "/Hack_font"])

    # refresh the fc-cache
    subprocess.run(["fc-cache", "-fv"])

    # removing temporary files
    subprocess.run(["rm", "--verbose", download_path])


def menage_temp_dir():

    # the default temp location
    # $HOME/temp <==
    temp_dir = USER_PATH + "/temp"

    # check temp
    if os.path.exists(temp_dir):

        # delete it
        subprocess.run(["rm", "-rfv", temp_dir])


def theme_installation():

    #########
    # THEME #
    #########

    # url
    mojave_git_url = "https://github.com/vinceliuice/Mojave-gtk-theme.git"

    # clone the repo
    subprocess.run(["git", "clone", mojave_git_url, USER_PATH + "/temp"])

    # execute the script
    subprocess.run(["sudo", "bash", USER_PATH + "/temp/install.sh",
                    "-d", USER_PATH + "/.themes",  # destination
                    "-n", "mojave-dark-solid",     # theme name
                    "-c", "dark",                  # color
                    "-o", "solid",                 # opacity
                    "-a", "standard",              # title-button
                    "-s", "small",                 # button-size
                    "-t", "grey",                  # other colors
                    "-i", "arch",                  # activities logo
                    "-g"])                         # gdm theme

    # deleting temporary files
    subprocess.run(["rm", "-rf", USER_PATH + "/temp"])


def icons_installation():

    #########
    # ICONS #
    #########

    # url
    zafiro_git_url = "https://github.com/zayronxio/Zafiro-icons.git"

    # isn't necessary delete  the temp dir, after theme_installation()

    # clone the repo
    subprocess.run(["git", "clone", zafiro_git_url, USER_PATH + "/temp"])

    # execute the script
    subprocess.run(["bash", USER_PATH + "/temp/Install-Zafiro-Icons.sh"])

    # deleting temporary files
    subprocess.run(["rm", "-rfv", USER_PATH + "/temp"])


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
                    "curl",                  # required
                    "cmake",                 # required
                    "cmatrix",               # fun
                    "cava",                  # music visualizer
                    "calibre",               # books manager
                    "dpkg",                  # required
                    "discord",               # chat
                    "default-jdk",           # ycm dependence
                    "flatpak",               # other pkgm
                    "git",                   # required
                    "golang",                # ycm dependence
                    "google-chrome-stable",  # browser
                    "gnome-tweaks",          # customization
                    "htop",                  # process viewer
                    "inkscape",              # images
                    "mono-complete",         # ycm dependence
                    "neofetch",              # the best
                    "nodejs",                # ycm dependence
                    "npm",                   # ycm dependence
                    "python3-dev",           # ycm dependence
                    "python3-pip",           # python pkgm
                    "vim-nox",               # ycm dependence
                    "vim",                   # text editor
                    "vlc",                   # video player
                    "telegram-desktop",      # chats
                    "tmux",                  # terminal mux
                    "wget"])                 # required


# call
if __name__ == "__main__":
    main()
