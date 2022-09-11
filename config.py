import os
import sys
import subprocess as sp

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
TEMP_FILE = USER_PATH + "/temp"

# error codes
ERRORS = dict()


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

    # network configuration
    # resolv_dns()

    system_apt_update()

    # programs installation
    # apt_programs_installation()
    # flatpak_programs_installation()

    # setting python
    # python_libs_installation()

    # various programs from the network
    # remove_temp()
    # musikcube_installation()
    theme_installation()
    # font_installation()
    # icons_installation()

    # symbolic links creation
    # create_symlinks()

    # programs configuration
    # vim_plugins_configuration()
    # tmux_plugins_configuration()

    # shows errors
    display_errors()

    # notification sound
    # notify()


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
        CNF_DIR+"/musikcube/hotkeys.json": SRC_DIR+"/musikcube/hotkeys.json",

        # calcurse/keys
        CNF_DIR+"/calcurse/keys": SRC_DIR+"/calcurse/keys"
    }

    for k, v in data.items():

        if not os.path.exists(v):
            ERRORS[v] = "doesn't exist"
            continue

        # always overwrite old files
        if os.path.exists(k):
            sp.run(["rm", "--verbose", k])

        # alacritty, maybe neofetch
        parent_dir = os.path.dirname(k)
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        # symlink creation
        try:
            os.symlink(v, k)
            print("Creating symlink.[SOURCE]:%s, [DEST]:%s"
                  % (v, k))
        except OSError as os_error:
            ERRORS["symlink"] = os_error


def resolv_dns():

    #######
    # DNS #
    #######

    target = "/etc/resolvconf/resolv.conf.d/head"
    source = SRC_DIR + "/dns/head"

    # remove old file
    sp.run(["sudo", "rm", "-v", target])

    # parent dir
    parent_dir = os.path.dirname(target)

    # copy the new file
    sp.run(["sudo", "cp", "-v",  source, parent_dir])

    # update resolv.conf
    sp.run(["sudo", "rm", "-v", "/etc/resolv.conf"])

    # create the symlink
    sp.run(["sudo", "ln", "-sv",
                    "../run/resolvconf/resolv.conf",
                    "/etc/resolv.conf"])
    # update
    sp.run(["sudo", "resolvconf", "-u"])


def notify():

    ################
    # NOTIFICATION #
    ################

    # fun notification
    from playsound import playsound
    playsound(SRC_DIR + "/notification/notification.wav")


def musikcube_installation():

    #############
    # MUSIKCUBE #
    #############

    # url (maybe it would be better to do something else)
    musikcube_releases = "https://github.com/clangen/musikcube/releases"
    musikcube_0_98_0 = "/download/0.98.0/musikcube_standalone_0.98.0_amd64.deb"
    musikcube_url = musikcube_releases + musikcube_0_98_0

    # wget deb file
    code = sp.run(["wget", "-O", TEMP_FILE, musikcube_url]).returncode

    # something went wrong, don't proceed
    if code:
        ERRORS["wget musikcube"] = code
        return  # don't proceed

    # installation
    code_2 = sp.run(["sudo", "dpkg", "-i", TEMP_FILE]).returncode
    if code_2:
        ERRORS["dpkg -i"] = code_2

    # remove temporary file
    sp.run(["rm", "-v", TEMP_FILE])


def font_installation():

    ########
    # FONT #
    ########

    # url (maybe it would be better to do something else)
    hack_releases_url = "https://github.com/ryanoasis/nerd-fonts/releases"
    version = "/download/v2.1.0/Hack.zip"
    hack_font_url = hack_releases_url + version

    # wget files
    code = sp.run(["wget", "-O", TEMP_FILE, hack_font_url]).returncode
    if code:
        ERRORS["wget hack nerd font"] = code
        return  # don't proceed

    # fonts dir
    fonts_dir = USER_PATH + "/.fonts"

    # if it doesn't exists, create.
    if os.path.exists(fonts_dir):
        sp.run(["rm", "-rfv", fonts_dir])
    os.mkdir(fonts_dir)

    # unzip the font
    code_2 = sp.run(["unzip", TEMP_FILE, "-d", fonts_dir +
                     "/hack-nerd-font"])
    if code_2:
        ERRORS["unzip hack nerd font"] = code_2
    else:
        # refresh the fc-cache
        code_3 = sp.run(["fc-cache", "-fv"])
        if code_3:
            ERRORS["fc-cache"] = code_3

    # removing temporary files
    sp.run(["rm", "-rfv", TEMP_FILE])


def remove_temp():

    # check temp
    if os.path.exists(TEMP_FILE):

        # delete it
        sp.run(["rm", "-rfv", TEMP_FILE])


def theme_installation():

    #########
    # THEME #
    #########

    # url (maybe it would be better to do something else)
    mojave_git_url = "https://github.com/vinceliuice/Mojave-gtk-theme.git"

    # clone the repo
    code = sp.run(["git", "clone",
                   mojave_git_url, TEMP_FILE]).returncode
    if code:
        return  # don't proceed

    # themes path
    themes_path = USER_PATH + "/.themes"

    # check if already exists
    if os.path.exists(themes_path):
        sp.run(["rm", "-rfv", themes_path])
    os.mkdir(themes_path)

    # execute the script
    code_2 = sp.run(["bash", TEMP_FILE + "/install.sh",
                     "-d", themes_path,  # destination
                     "-n", "mojave-dark-solid",     # theme name
                     "-o", "solid",                 # opacity
                     "-a", "standard",              # title-button
                     "-s", "small",                 # button-size
                     "-t", "grey",                  # other color
                     "-i", "arch"])                 # activities logo
    # "-c", "dark",                  # color
    if code_2:
        ERRORS["themes_install.sh"] = code_2

    # removing temporary files
    sp.run(["rm", "-rfv", TEMP_FILE])


def icons_installation():

    #########
    # ICONS #
    #########

    # url (maybe it would be better to do something else)
    zafiro_git_url = "https://github.com/zayronxio/Zafiro-icons.git"

    # clone the repo
    code = sp.run(["git", "clone",
                   zafiro_git_url, TEMP_FILE]).returncode
    if code:
        ERRORS["git clone zafiro"] = code
        return  # don't proceed

    # default user icons path
    icons_path = LCL_SHARE_DIR + "/icons"

    # if exists, delete it
    if os.path.exists(icons_path):
        sp.run(["rm", "-rfv", icons_path])
    os.mkdir(icons_path)

    # execute the script
    code_2 = sp.run(["bash", TEMP_FILE + "/Install-Zafiro-Icons.sh"])
    if code_2:
        ERRORS["icons_install.sh"] = code_2

    # deleting temporary files
    sp.run(["rm", "-rfv", TEMP_FILE])


def system_apt_update():

    #################
    # SYSTEM UPDATE #
    #################

    sp.run("sudo apt update && sudo apt upgrade", shell=True)


def vim_plugins_configuration():

    ##############################
    # VIM PLUGINS CONFIGURATION  #
    ##############################

    # default vundle dir
    vundle_path = USER_PATH + "/.vim/bundle/Vundle.vim"

    # remove old vundle dir if exists
    if os.path.exists(vundle_path):
        sp.run(["rm", "-rfv", vundle_path])

    # clone vundle
    code = \
        sp.run(["git", "clone",
                "https://github.com/VundleVim/Vundle.vim.git",
                vundle_path]).returncode

    # plugins installation
    if not code:
        code_2 = sp.run(["vim", "-c",
                         "PluginInstall",
                         "+qall"]).returncode
        # ycm installation
        if not code_2:
            code_3 = sp.run([USER_PATH + "/.vim/bundle/YouCompleteMe/" +
                             "install.py", "--all"]).returncode
            if code_3:
                ERRORS["ycm install.sh"] = code_3
        else:
            ERRORS["vim PluginInstall"] = code_2
    else:
        ERRORS["git clone vundle"] = code


def tmux_plugins_configuration():

    ##############################
    # TMUX PLUGINS CONFIGURATION #
    ##############################

    # default tmux dir
    tpm_path = "/.tmux/plugins/tpm"

    # remove old tpm dir if exists
    if os.path.exists(USER_PATH + tpm_path):
        sp.run(["rm", "-rfv", USER_PATH + tpm_path])

    # clone tpm
    code = sp.run(["git", "clone",
                   "https://github.com/" +
                   "tmux-plugins/tpm",
                   USER_PATH + tpm_path]).returncode
    # refresh tmux envirnment
    if not code:
        code_2 = sp.run(["tmux", "source",
                         USER_PATH +
                         "/.tmux.conf"]).returncode
        # plugins installation
        if not code_2:
            code_3 = sp.run(["bash", USER_PATH + "/.tmux/plugins/" +
                             "tpm/scripts/" + "install_"
                             + "plugins.sh"]).returncode
            if code_3:
                ERRORS["tpm plugin.sh"] = code_3
        else:
            ERRORS["tmux source"] = code_2
    else:
        ERRORS["git clone tpm"] = code


def flatpak_configuration():

    #########################
    # FLATPAK CONFIGURATION #
    #########################

    # add flathub repository
    code = sp.run(["flatpak", "remote-add", "--if-not-exists",
                   "https://flathub.org/repo/flathub.flatpakrepo"]).returncode
    if code:
        ERRORS["flathub"] = code


def flatpak_programs_installation():

    #########################
    # PROGRAMS FROM FLATPAK #
    #########################

    # flathub repository
    flatpak_configuration()

    # programs installation
    sp.run(["flatpak", "install", "flathub",
            "org.eclipse.java"])


def apt_programs_installation():

    #####################
    # PROGRAMS FROM APT #
    #####################

    sp.run(["sudo", "apt", "install",
            "acpi",                  # battery shower
            "alacritty",             # terminal
            "build-essential",       # ycm dependence
            "calcurse",              # terminal calendar
            "calibre",               # books manager
            "cava",                  # music visualizer
            "cmake",                 # required
            "cmatrix",               # fun
            "curl",                  # required
            "emacs",                 # just emacs
            "default-jdk",           # ycm dependence
            "discord",               # chat
            "dpkg",                  # required
            "fim",                   # image visualizer
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


def python_libs_installation():

    ############################
    # PYTHON LIBS INSTALLATION #
    ############################

    # python libs
    code = sp.run(["pip", "install",
                   "Matplotlib",     # comment here
                   "NumPy",          # comment here
                   "ddt",            # comment here
                   "flake8",         # comment here
                   "pillow",         # comment here
                   "playsound",      # comment here
                   "pyfiglet",       # comment here
                   "pypi-json",      # comment here
                   "requests"])      # comment here
    if code:
        ERRORS["pip"] = code


def display_errors():

    ##################
    # DISPLAY ERRORS #
    ##################

    if ERRORS:
        print("==============ERRORS================")
    for k, v in ERRORS.items():
        print("context: %s | error code: %s" % (k, v))


# call
if __name__ == "__main__":
    main()
