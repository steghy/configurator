"########################################
"	VIM CONFIGURATION FILE          #
"########################################
"
" required (vundle stuff)
set nocompatible
filetype off

" lines number
set relativenumber

" split screen
set splitbelow
set splitright

" encode
set encoding=UTF-8

" Enable folding
set foldmethod=indent
set foldlevel=9
:
" Enable the mouse
set mouse=a

" vim update time
set updatetime=1000

" Not necesary
map <C-c> <Nop>

" copy and paste section noremap <Leader>y "*y noremap <Leader>p "*p
noremap <Leader>Y "+y
noremap <Leader>P "+p

" docstrings for folded code
let g:SimpylFold_docstring_preview=1

" close auto-complete automatically
let g:ycm_autoclose_preview_window_after_completion=1

" colors (It doesn't do much)
highlight Pmenu ctermfg=15 ctermbg=0 guifg=#ffffff guibg=#000000

" Python Syntax
let python_highlight_all=1

syntax on

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

" When invoked, unless a starting directory is specified, CtrlP will set its
" local working directory according to this variable
let g:ctrlp_working_path_mode = 'ra'

" indentation lines color
" let g:indentLine_color_term = 239
" let g:indentLine_char_list = ['|']

" powerline always active
set laststatus=2

"########
" FOLDS #
"########

nnoremap <space> za
map za <Nop>

"########################
"                       #
" PLUGINS INSTALLATION  #
"                       #
"########################

call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" Folds
Plugin 'tmhedberg/SimpylFold'

" Indentations
Plugin 'vim-scripts/indentpython.vim'

" Syntax
Plugin 'nvie/vim-flake8'

" Dense-Analysis/ALE
Plugin 'dense-analysis/ale'

" Whitespace
Plugin 'bitc/vim-bad-whitespace'

" Auto-completation
Plugin 'Valloric/YouCompleteMe'

" Doc-strings
Plugin 'pixelneo/vim-python-docstring'

" File browsing
Plugin 'scrooloose/nerdtree'

" Search anything
Plugin 'kien/ctrlp.vim'

" Powerline
Plugin 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}

" Parentheses, Brackets ecc..
Plugin 'tpope/vim-surround'

" Indentation lines
" Plugin 'Yggdroot/indentLine'

" Cool icons
" Plugin 'yanoasis/vim-devicons'

call vundle#end()

"##########################
"                         #
" TERMINAL CONFIGURATION  #
"                         #
"##########################

" terminal
nnoremap <C-t> :term<CR>

" the current dir of the terminal
nnoremap <C-t> :let $VIM_DIR=expand('%:p:h')<CR>:term<CR>cd $VIM_DIR<CR>


"#########################
"                        #
" NERDTREE CONFIGURATION #
"                        #
"#########################

" close NERDTree automatically when a file is open
let g:NERDTreeQuitOnOpen = 1

" let nerdtree to shows hidden files
let NERDTreeShowHidden=1

let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1

" Open-Close NERDTree with C-n
nmap <C-n> :NERDTreeToggle<CR>

" start NERDTree, unless a file or session is specified, eg. vim -S session_file.vim.
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists('s:std_in') && v:this_session == '' | NERDTree | endif

" exit Vim if NERDTree is the only window remaining in the only tab.
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

" split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

"########################
"                       #
" 	SWAP FILES      #
"                       #
"########################

set directory=~/.vim/swap//

" required (Vundle stuff)
filetype plugin indent on
