
If you have a piece of code that takes a long  time to complete e.g. a neural network that needs a day to train, a script that needs to download a million papers, a web scraper that needs to wait 10 seconds before recontacting a server (repeated 300,000 times) you will find you working remotely a bit frustrating. When you close your laptop it can disconnect. Or your internet at home is awful. Either way you send your script running overnight and come back in the morning to find the terminal disconnect and cancelled your script. All that time wasted because the connection between you and the server disconnected. 

What we want is to let our scripts/code run and the code to persist even if our terminal session ends. Luckily there are tools in linux that allow us to do this. There are three that I know of
- `nohup`
- `screen`
- `tmux`

Previously I have only used `nohup`. In some ways it is the simplest method. But today I am going to try use propaganda to convert you to `tmux`.


# nohup
Run a script in the background that will persist after disconnecting.

```bash
nohup python myscript.py > output.log 2>&1 & # run myscript.py in the background
echo $! > save_pid.txt # save pid of that process so we can cancel the script easily
```
Check the output 
```bash
tail -f output.log # -f lets us see "live" output from our script
```

Kill the script with
```bash
kill -9 `cat save_pid.txt` # cancel the process associated with our script
rm save_pid.txt # remove the file where we stored the pid afterwards
```

Below I will explain what these commands do and why they are helpful. 

>Note: commands discovered through this [stack overflow answer](https://stackoverflow.com/questions/17385794/how-to-get-the-process-id-to-kill-a-nohup-process)

## getting started
`nohup` is a command that tells your script to ignore the hang up signal that occurs when a terminal window is closed (in our case when our laptop disconnects from the server). It stands for "no hang up". In practice, it is very simple to run. You simply add nohup in front of your normal script/command e.g.

```
nohup python trainmymodel.py
nohup ./mybashscript.sh
```

When you do that you will find the process runs even if you disconnect or close the terminal. You can still cancel the command with keyboard interrupt (ctrl+c). 

### script output
If you run nohup you will find the output of any script e.g. print('hello world') will not appear. This is because all standard output is redirected to nohup.out, a file that is created when you run the command nohup. This is so you can still see the output of a script after you disconnect. You can change the name/specify the output file by using the ["redirect" operator](https://unix.stackexchange.com/questions/171025/what-does-do-vs)  `>` (second answer is clearer).

```bash
nohup python trainmymodel.py > output.log
```

This will send all output from our script into output.log. 

#### standard error
The above script works great but you will find if any errors occur they will not appear. This is because the terminal has two separate ways of outputting
1. `stdout` - standard output  (normal output from scripts or commands)
2. `stderr` - standard error (output caused by any errors). 
In your terminal both of these appear the same and show up identically but you actually have to access them separately. 

>Note: this is designed this way so admin or server host or people doing more complicated computer things can check just for errors rather than dealing with all output. 

To get the standard error to output to our output file we use 
```bash
nohup python trainmymodel.py > output.log 2>&1
```

`2>&1` tells standard error (output channel 2) to output instead through channel 1 (standard output). If we wanted error to go to a separate file we could use
```
nohup python trainmymodel.py > output.log 2>error.log
```
A more detailed and more comprehensive explanation of the way you can manipulate linux output is [here](https://tldp.org/LDP/abs/html/io-redirection.html).  

#### append rather than overwrite
The last thing I should tell you is that we can append output to an existing log using `>>`.
Here we use  `> output.log` which overwrites our output. If instead we wanted to keep the previous log we can use `>>`
```bash
nohup python trainmymodel.py >> output.log 2>&1
```
Here we append output all output to the existing `output.log` file rather than overwriting. 

> Note: `2>&1` doesn't change. This is because we are redirecting stderr through stdout and when we do this we don't create or overwrite output files. 

### running in background
While running with nohup means our script will not be cancelled when we disconnect it does mean our terminal cannot be used or we can accidently cancel our script with keyboard interrupt (ctrl+c). 
To ensure our script does not get interrupted we can run our code in the background using `&`
```bash
nohup python trainmymodel.py > output.log  2>&1 & 
```
Now our script cannot be interrupted. For an nice explanation of the different ways processes in the terminal can be interrupted see this [stack overflow post](https://stackoverflow.com/questions/55110150/nohup-vs-nohup).
#### killing process
The next question is how to kill our background process. Using keyboard interrupt or disconnecting won't work. We need to kill the process directly.  To do this we have two steps. 
1. find the process id (`pid`)
2. kill the process manually

To find current active process we can use
```bash
ps aux 
```
This lists all process associated with the current user (i.e. your processes). We can search for a particular process using `grep`.
```bash
ps aux | grep "insertnameofscripthere"
```
So we could use
```bash
ps aux | grep "trainmymodel"
```
to find the `pid` that would occur if we used one of the example commands above.

Once we have the pid we can end the process using the `kill` command 
```
kill -9 putpidnumberhere
```
e.g. `kill -9 1234`

### Automatically finding process id
We can automatically find the process id and store it. You might notice that immediately after we run the command a pid appears. We can display that pid using
```bash
echo $! 
```
`$!` displays the last process executed (note this pid might not show up if `&` is not used. I don't fully understand the command)
We can store the pid in a file using
```bash
echo $! > save_pid.txt
```
We can then kill the process 
```
kill -9 `cat save_pid.txt`
```
First cat prints the contents of save_pid.txt i.e. our pid, then we kill the process.


# tmux
Nohup is great but it can be a bit frustrating when trying to develop a script as errors appear in a separate output file. A nice alternative is `tmux` . It allows you to run terminal sessions in the background. So rather than nohup which ensures a script keeps running after you exit the terminal, tmux allows you to detach from a terminal session and continue later as if you never left. 

It also add two great additional features - windows (essentially tabs within the terminal) and panes (allow you to split the screen and have multiple terminal instances in one window).

I really like as it allows me to reconnect to the server and use one command to rejoin a terminal session that has already opened all the folders I might end up working from. 
For example, I connect and I have one window in my `phd-thesis` repository (active code), one in my `docs` repository (where I keep notes), one in my home repository (`~/`) and one in my data folder (checking results etc).

I can also have another session with active scripts that I sent running the night before. So with command I hop to the other tmux session and can check how they progressed. 

I think the functionality is really good and I personally have found it very very useful.

## tmux commands
This is a mixture of cheat sheet and guide of how to start tmux. I recommend this [guide](https://medium.com/hackernoon/a-gentle-introduction-to-tmux-8d784c404340) and this [cheatsheet](https://gist.github.com/MohamedAlaa/2961058) for a more in depth walkthrough of `tmux`. I think the [official getting started guide](https://github.com/tmux/tmux/wiki/Getting-Started) is also great. They have some nice images explaining the terminal and go into much better depth of all of tmux's features than I have (there is advanced copy paste tools I haven't explored).

### install on ubuntu
```bash
sudo apt-get update # first refresh package list
sudo apt-get install tmux # then install tmux
```
Note: big.inf.ed.ac.uk already has `tmux` installed

See [tmux guide for installation](https://github.com/tmux/tmux/wiki/Installing) on other distributions/OS.

### Create and manage sessions
create new session
```bash
tmux 
```
exit
```
ctrl+d
```

list active session
```bash
tmux ls
```

kill session by name -t means target
```bash
tmux kill-ses -t 1
```
create new named session
```bash
tmux new -s mysession
```

detach from session
```
ctrl+b d
```

list all session
```
tmux ls 
```

reattach to mysession
```bash
tmux a -t mysession
```

name session
```
ctrl+b $
```

### windows
create new window
```
ctrl+b c
```
rename window
```
ctrl+b , 
```
move to next window
```
ctrl+b n
```
move to previous window
```
ctrl+b p
```
kill window
```
ctrl+b &
```

### panes
horizontal split on current window
```
ctrl+b %
```

swap panes
```
ctrl+b o
```

move between panes using arrow keys
```
ctrl+b →
ctrl+b ←
```

show pane numbers
```
ctrl+b q
```
kill pane
```
ctrl+b x
```


>Note: turning on mouse-mode is helpful especially when starting off. Use `ctrl+b :` to enter `set-option` mode then type `set -g mouse on` . See below for how to enable mouse-mode by default in the config.


## Customising tmux 
This is entirely optional so ignore if you like.

To edit the tmux config and customise the visuals of tmux you add commands to `~/.tmux.conf`. To edit the file in vscode simply type 
```
code ~/.tmux.conf 
```

If you make some changes e.g. turn on mouse mode by default (adding `set -g mouse on` to `.tmux.conf`) then you will need to refresh the tmux settings. One way is to close terminal and reconnect.

Another is 
```bash
tmux source-file ~/.tmux.conf
```
this is similar to refreshing bash setting by using source `~/.bashrc`.

Below is the contents of my `.tmux.conf` . Most of it is aestethic but  **note:** *I change the command hotkey from `ctrl+b` to `ctrl+a`*


Here is the full list of the changes  contained in the code below
- **mouse mode** - turn on mouse mode so I can click between windows & panes
- **new hotkey** - change command hotkey from `ctrl+b` to `ctrl+a` (only because I find easier to type with one hand)
- **enable colours** 
- **move status bar** - from bottom to to top 
- **window index** - start counting windows from 1 rather than 0
- **new colors** - changed colours (from green) and added some different formatting (entirely personal preference)


My `~/.tmux.conf`:

```bash
# turn on colors
set -g default-terminal "xterm-256color" # Setting the correct term

# change tmux command binding to ctrl+a rather than ctrl+b
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix

# turn on mouse mode
set -g mouse on

# change index to start from 1
set -g base-index 1

# Update the status line every second
set -g status-interval 1

# statusbar
## position of bar and window lists
set -g status-position top # [top | bottom]  status bar
set -g status-justify left # [left | centre | right]  window lists
## colours & format
set -g status-style 'bg=blue fg=yellow'
set -g status-left ''
set -g status-right '#[fg=colour233,bg=cyan] %d/%m #[fg=colour233,bg=magenta] %H:%M:%S '
set -g status-right-length 50
set -g status-left-length 20
# ^colour233 is a shade of grey that looked nice

# set inactive window format and color
set -g window-status-style 'fg=black, bg=brightblue'
set -g window-status-format ' #I: #W #F'

# set active window format and color
setw -g window-status-current-style 'fg=colour233, bg=yellow bold'
set -g window-status-current-format ' #I: #W #F'
# ^when setting format #F displays a * if in active window and - if not. 
#          #I is the index of the window, #W is the window name
```


