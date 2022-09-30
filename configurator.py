import os
import sys
import subprocess as sp

#############################
# CONFIGURATOR.             #
# steghy                    #
# steghy.github@proton.me   #
#############################

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

CWD = os.getcwd()

# error codes
ERRORS = dict()


def main():

    ########
    # MAIN #
    ########

    if os.geteuid() == 0:
        sys.exit("don't run this script as a root!")

    #  network configuration
    resolv_dns()

    system_apt_update()

    # programs installation
    apt_programs_installation()

    # setting python
    python_libs_installation()

    # various programs from the network
    remove_temp()
    musikcube_installation()
    theme_installation()
    font_installation()
    icons_installation()

    # symbolic links creation
    create_symlinks()

    # programs configuration
    vim_plugins_configuration()
    tmux_plugins_configuration()
    bash_configuration()

    # import custom shortcuts
    imp_cs_gnome()

    # shows errors
    display_errors()

    # notification sound
    notify()


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

        if os.path.exists(k):
            sp.run(["rm", "-v", k])

        parent_dir = os.path.dirname(k)
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

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
    source = CWD + "/dns-servers"

    if not os.path.exists(source):
        ERRORS["./dns-servers"] = "not exists"
        return

    # echo -e "nameserver 8.8.8.8\nnameserver 8.8.4.4" >> target ?
    code = sp.run(["sudo", "rm", "-v", target]).returncode

    if not code:
        parent_dir = os.path.dirname(target)

        code_2 = sp.run(["sudo", "cp",
                         "-v",  source, parent_dir]).returncode

        if not code_2:
            code_3 = sp.run(["sudo", "rm",
                             "-v", "/etc/resolv.conf"]).returncode
            if not code_3:
                code_4 = sp.run(["sudo", "ln", "-sv",
                                 "../run/resolvconf/resolv.conf",
                                 "/etc/resolv.conf"]).returncode
                if not code_4:
                    code_5 = sp.run(["sudo", "resolvconf", "-u"]).returncode
                    if code_5:
                        ERRORS["resolvconf -u"] = code_5
                else:
                    ERRORS["dns: ln -s"] = code_4
            else:
                ERRORS["rm etc/resolv.conf"] = code_3
        else:
            ERRORS["cp %s to %s" % (source, parent_dir)] = code_2
    else:
        ERRORS["dns: rm head"] = code


def notify():

    ################
    # NOTIFICATION #
    ################

    # fun notification
    from playsound import playsound
    playsound(CWD + "/notification.wav")


def musikcube_installation():

    #############
    # MUSIKCUBE #
    #############

    # url (maybe it would be better to do something else)
    musikcube_releases = "https://github.com/clangen/musikcube/releases"
    musikcube_0_98_0 = "/download/0.98.0/musikcube_standalone_0.98.0_amd64.deb"
    musikcube_url = musikcube_releases + musikcube_0_98_0

    code = sp.run(["wget", "-O", TEMP_FILE, musikcube_url]).returncode

    if code:
        ERRORS["wget musikcube"] = code
        return

    code_2 = sp.run(["sudo", "dpkg", "-i", TEMP_FILE]).returncode
    if code_2:
        ERRORS["dpkg -i"] = code_2

    sp.run(["rm", "-v", TEMP_FILE])


def font_installation():

    ########
    # FONT #
    ########

    # url (maybe it would be better to do something else)
    hack_releases_url = "https://github.com/ryanoasis/nerd-fonts/releases"
    version = "/download/v2.1.0/Hack.zip"
    hack_font_url = hack_releases_url + version

    code = sp.run(["wget", "-O", TEMP_FILE, hack_font_url]).returncode
    if code:
        ERRORS["wget hack nerd font"] = code
        return

    fonts_dir = USER_PATH + "/.fonts"

    if os.path.exists(fonts_dir):
        sp.run(["rm", "-rfv", fonts_dir])
    os.mkdir(fonts_dir)

    code_2 = sp.run(["unzip", TEMP_FILE, "-d", fonts_dir +
                     "/hack-nerd-font"]).returncode
    if code_2:
        ERRORS["unzip hack nerd font"] = code_2
    else:
        code_3 = sp.run(["fc-cache", "-fv"]).returncode
        if code_3:
            ERRORS["fc-cache"] = code_3

    sp.run(["rm", "-rfv", TEMP_FILE])


def theme_installation():

    #########
    # THEME #
    #########

    mojave_git_url = "https://github.com/vinceliuice/Mojave-gtk-theme.git"
    code = sp.run(["git", "clone",
                   mojave_git_url, TEMP_FILE]).returncode
    if code:
        return

    themes_path = USER_PATH + "/.themes"

    if os.path.exists(themes_path):
        sp.run(["rm", "-rfv", themes_path])
    os.mkdir(themes_path)

    code_2 = sp.run(["bash", TEMP_FILE + "/install.sh",
                     "-d", themes_path,             # destination
                     "-n", "mojave-dark-solid",     # theme name
                     "-o", "solid",                 # opacity
                     "-a", "standard",              # title-button
                     "-s", "small",                 # button-size
                     "-t", "grey",                  # other color
                     "-i", "arch"]).returncode      # activities logo

    if code_2:
        ERRORS["themes_install.sh"] = code_2

    sp.run(["rm", "-rfv", TEMP_FILE])


def icons_installation():

    #########
    # ICONS #
    #########

    # url (maybe it would be better to do something else)
    zafiro_git_url = "https://github.com/zayronxio/Zafiro-icons.git"

    code = sp.run(["git", "clone",
                   zafiro_git_url, TEMP_FILE]).returncode
    if code:
        ERRORS["git clone zafiro"] = code
        return

    icons_path = LCL_SHARE_DIR + "/icons"

    if os.path.exists(icons_path):
        sp.run(["rm", "-rf", icons_path])
    os.mkdir(icons_path)

    code_2 = sp.run(["bash", TEMP_FILE + "/Install-Zafiro-Icons.sh"])
    if code_2:
        # error code 1 (rm github.com fail, bad script)
        ERRORS["icons_install.sh"] = code_2

    sp.run(["rm", "-rf", TEMP_FILE])


def system_apt_update():

    #################
    # SYSTEM UPDATE #
    #################

    sp.run("sudo apt update && sudo apt upgrade", shell=True)


def bash_configuration():

    ######################
    # BASH CONFIGURATION #
    ######################

    code = sp.run("sudo curl -sS https://starship.rs/install.sh"
                  "| sh", shell=True).returncode
    if code:
        ERRORS["curl starship"] = code

    bashrc_config = SRC_DIR + "/bash/bashrc-config"
    bashrc = USER_PATH + "/.bashrc"
    if os.path.exists(bashrc_config):
        if os.path.exists(bashrc):
            data = ""
            with open(SRC_DIR + "/bash/bashrc-config", mode='r') as file:
                data = file.read()
            with open(USER_PATH + "/.bashrc", mode='a') as file:
                file.write(data)
        else:
            ERRORS["~/.bashrc"] = "not exists"
    else:
        ERRORS["config/bashrc-config"] = "not exists"


def vim_plugins_configuration():

    ##############################
    # VIM PLUGINS CONFIGURATION  #
    ##############################

    vundle_path = USER_PATH + "/.vim/bundle/Vundle.vim"

    if os.path.exists(vundle_path):
        sp.run(["rm", "-rfv", vundle_path])

    code = \
        sp.run(["git", "clone",
                "https://github.com/VundleVim/Vundle.vim.git",
                vundle_path]).returncode

    if not code:
        code_2 = sp.run(["vim", "-c",
                         "PluginInstall",
                         "+qall"]).returncode
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

    tpm_path = "/.tmux/plugins/tpm"

    if os.path.exists(USER_PATH + tpm_path):
        sp.run(["rm", "-rfv", USER_PATH + tpm_path])

    code = sp.run(["git", "clone",
                   "https://github.com/" +
                   "tmux-plugins/tpm",
                   USER_PATH + tpm_path]).returncode
    if not code:
        code_2 = sp.run(["tmux", "source",
                         USER_PATH +
                         "/.tmux.conf"]).returncode
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


def apt_programs_installation():

    #####################
    # PROGRAMS FROM APT #
    #####################

    sp.run(["sudo", "apt", "install",
            "acpi",                  # battery shower
            "alacritty",             # terminal
            "ant",                   # Apache ant
            "audacity",              # audacity
            "build-essential",       # ycm dependence
            "calcurse",              # terminal calendar
            "calibre",               # books manager
            "cmake",                 # required
            "curl",                  # required
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

    code = sp.run(["pip", "install",
                   "Matplotlib",     # comment here
                   "NumPy",          # comment here
                   "ddt",            # comment here
                   "flake8",         # comment here
                   "pillow",         # comment here
                   "playsound",      # comment here
                   "pyfiglet",       # comment here
                   "pypi-json",      # comment here
                   "requests"]).returncode
    if code:
        ERRORS["pip"] = code


def imp_cs_gnome():

    ####################
    # CUSTOM SHORTCUTS #
    ####################

    code = sp.run("dconf load / < custom-shortcuts.conf",
                  shell=True).returncode
    if code:
        ERRORS["dconf load"] = code


def display_errors():

    ##################
    # DISPLAY ERRORS #
    ##################

    if ERRORS:
        print("> Errors:")
    for k, v in ERRORS.items():
        print("context: %s | error code: %s" % (k, v))


def remove_temp():
    if os.path.exists(TEMP_FILE):
        sp.run(["rm", "-rfv", TEMP_FILE])


if __name__ == "__main__":
    main()
