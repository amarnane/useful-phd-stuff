# Remote working
I really like working on a remote server. I find there are a number of benefits over coding locally that are worth taking the time to set it all up. 
- The main one: I can **work wherever I want**. Either on my desktop machine or on my laptop and I can always access the the same environment. I don't have to worry if I installed something new on one machine or if I moved the correct data around. It all stays in the same place and I can access it as I need. 
- The second benefit is **running a long program**. If something takes a couple of hours or days, you don't need to worry about shutting down and moving your laptop or having to deal with lag because of memory issues while you wait (I am very impatient). 
- Lastly,  **more ram, more memory, more fun**. 


## VSCode
The main tool I use to work remotely is [vscode](https://code.visualstudio.com/). VSCode is an IDE developed by microsoft. It is lightweight, there are a lot of extensions that make coding nice and it has a great setup for remote work. I believe Pycharm has a similar setup and as students we can get a licence but honestly my main problem is it takes ages to open up and I am a true believer in making things as smooth as possible to start work (otherwise procrasination can take over).

### Using vscode to work remotely
Running vscode on a remote computer or server is very simple. There are 3 steps
1. install [remote server extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
2. add server details to `.ssh/config`. The simplest way is to
	1. `ctrl+shift+p` Remote-SSH: Add New SSH Host
	2. type ssh connection e.g. `ssh username@server.address`
	3. An entry has now been made to your `ssh config` (will explain below)
3. Connect to server using  `ctrl+shift+p` Remote-SSH: Connect to Host

After that you just open a folder/file and can code away with all code running remotely. 

### Tips for Remote Work
Some tips I find helpful. 
- Only write code in github repos and commit regularly! So important to have a backup. If something goes wrong the code is gone forever! Plus if you don't like changes you make you can revert to code you wrote 3 months ago. 
- Add your public key from your local computer to the accepted keys on the server so you don't have to type passwords again and again. Do same thing for git, add public key to [accepted keys on github](https://github.com/settings/keys). *(links to guides down below)*
- I like doing analysis in jupyter notebooks but I often find they get cluttered, messy and it is tedious to look back through notebooks and access functions or scripts that I wrote. Good practice is to move functions/classes you use regularly to `.py` as source code and create scripts that accept command line arguments for specific tasks you will want to do. *(again a small guide down below)*
- Use `rsync` to move data from your computer to the server and vice versa. 
	- `rsync -azP source destination`
		- `-z` flag compresses the data as it is copied so is very efficient. 
		- `-a` flag,which stands for archive, syncs recursively and allows to transfer folders. Is similar to `-r` flag but keeps permissions, timestamps, ownership and other things (more likely to stop things breaking). 
		- `-P` gives progress bar and resumes interrupted transfers.
	- Format is `rsync -azP local_path_2_folder username@server.address:path_on_remote_server` e.g. `rsync -azP ~/dir1 amarnane@big.inf.ed.ac.uk:~/docs/` (flip order to move from remote to local)
	- There are many more options that I haven't explored yet but this [a nice tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories)
- This is a general PhD thing but write out thoughts in notebooks, comment regularly in your code and try to datestamp or include copy of the code used to generate any figures or models or data. At some point you will drop what you are working on or need to come back to something after a couple of months/years and you will not remember what exactly it was you did. Make it easier for yourself! *I have some code for appending dates to filenames and backing up source code if you want it just send me a message or I can include them in this document?* 
- **Next step/Advanced/I have not done this**: 
	- Use [docker](https://www.docker.com/) instances so that you can easily share your environment/model and have it run right away. It  allows you to save a copy of your setup so people can just run your code e.g. run a model developed on linux in a windows machine. 
	- Use a workflow system like [snakemake](https://snakemake.readthedocs.io/en/stable/) or [nextflow](https://www.nextflow.io/) to combine scripts and make and end to end pipline for your project. If you have multiple steps like preprocess data -> create data stucture -> train model -> analyse output you can combine them easily using a workflow system and pass the output from one section to the other easily. It is more modular and adaptable than writing an end to end script (if your code is python only) and allows you to pass output from one language to a script using different software e.g. python train model, R analyse and plot. Can also add checkpoints to start the pipeline from any intermediate step e.g. change model and skip rerunning preprocessing.


## ssh connections
`ssh` or [Secure shell](https://geekflare.com/understanding-ssh/) is a protocol used to access remote computers over a network. The link will describe it better than I can but the main thing to know is that it is a way to access other computers in a safe way. It is very secure and as a phd student the main thing to know is you can use it work remotely, create passwordless connections and passwordless git repos. If you ever want to use a cluster or connect to the biginf server, `ssh` is the way to do it. On linux the connections are done through the terminal (or vscode as I described above). On windows, it used to be a bit trickier but you can now access it through [powershell](https://lazyadmin.nl/powershell/powershell-ssh/) and vscode. 

To connect to a remote computer you go to the terminal and type the simple command
```
ssh username@server.addresss
```
So to connect to `biginf` I type
```
ssh amarnane@big.inf.ed.ac.uk
```
You will then receive a prompt to enter my password and are connected. 

### Adding authorised keys
First check what keys/files exist in your .ssh folder
```
ls ~/.ssh
```
ssh keys will look something like
```
id_ed25519          id_ed25519.pub         id_rsa      id_rsa.pub
```
They are public/private pairs. Never share your private key. The public key is shared with remote systems (biginf or github) so they can check it matches the private key when you connect.

If no keys are present you will need to generate keys. The names `rsa`/`ed25519` are names of algorithms for  generate keys. `rsa` was the most common but is now quite old. `ed25519` is more secure and recommended. If you do use `rsa`, it is recommended to create one with higher bits. The commands you will commonly see are 
```
ssh-keygen -t rsa -b 4096
ssh-keygen -t ed25519
```
`-b` here specifies the size of the key in bits. Pick one and now an `id_rsa` or `id_ed25519` private&public pair will be present in your `.ssh` folder. A nice explanation of the algorithms and keys in general can be found [here](https://www.ssh.com/academy/ssh/keygen#choosing-an-algorithm-and-key-size).

We now want to add our public key to the authorized keys in the remote server. First we need to copy the public key to the server
```
scp ~/.ssh/id_ed25519.pub username@server.address:~/
```
(we could use `rsync` here as shown above. `scp` works similarly.)

We then need to connect to the server
```
ssh username@server.address
```
We are now on the remote server. First check `id_ed25519.pub` was copied successfully,
```
ls ~/
```
Now check if our authorized_keys file exists
```
ls ~/.ssh
```
If it doesn't exist we need to create it
```
touch ~/.ssh/authorized_keys
```
touch is a helpful command that creates an empty text file. The authorized_keys file is simply a list of public keys. We you connect using ssh it checks if your key private key against the public keys stored in the authorized key list, if its a match you can connect.

Now we want to add our public key to the authorized key list
```
cat ~/id_ed25519.pub >> ~/.ssh/authorized_keys
```
`cat` displays the contents of a file (in this case our public key) and  `>>` pipes it into a file. So instead of seeing the output of the file in terminal, it is placed in the `authorized_keys` file. Note: `>>` appends to the end of the file. We could also use `>` but this writes to file and would overwrite the content in `authorized_keys`.

### Other links
- [Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to add ssh key to your github account (passwordless git commit, push, pull etc)
- [More in depth guide](https://kb.iu.edu/d/aews) to add ssh key to authorized keys to allow passwordless ssh connections 


## ssh config
I discovered the `ssh config` through vscode (it is how it handles remote connections) but it is incredibly useful. It is particularly useful for complex `ssh` commands that involve a number of options like [portforwarding](https://ljvmiranda921.github.io/notebook/2018/01/31/running-a-jupyter-notebook/) or use a proxy to connect to a server. It really slims down how much you have to type and how many usernames server address etc you have to remember. The format is very simple. You write out the options for your connections and give it a name.

So instead of 
```
ssh username@server.address
```
You can type
```
ssh myserver 
```
By adding
```
Host myserver
    HostName server.address
    User username
```
to the config.

### Creating the config file
First check the config file exists, your config should be located at ~/.ssh/config
ls ~/.ssh
If not create it using touch
touch ~/.ssh/config
The config file is simply a text file that has a specific format
```
Host hostname1
    SSH_OPTION value
    SSH_OPTION value

Host hostname2
    SSH_OPTION value
```

### Example connection
Here is an example of my setup to allow me to connect to `big.inf.ed.ac.uk`
```
Host biginf
    HostName big.inf.ed.ac.uk
    User amarnane
    ServerAliveInterval 30
```
Where I have made `ServerAliveInterval` smaller than default to try reduce the number of disconnects that happen while I work.

So now if I want to connect via `ssh` or copy files from my computer to the server I can just use `biginf`. For example moving public key to the server
```
scp ~/.ssh/id_ed25519.pub biginf:~/
```

***insert example proxyjump for connecting to eddie here***

### Useful Links
- Some more in depth guides for the config are [here](https://linuxize.com/post/using-the-ssh-config-file/)(I find this one easier to follow) and [here](https://www.digitalocean.com/community/tutorials/how-to-configure-custom-connection-options-for-your-ssh-client)
- List of all possible options to add to the [config](https://man7.org/linux/man-pages/man5/ssh_config.5.html)


## Connecting outside DICE
If you try any of the advice above using your laptop you will likely encounter a problem. You cannot connect to `big.inf.ed.ac.uk` or any other informatics server. The reason for this is the informatics firewall. It is separate from the rest of the university network and **requires the informatics vpn** to connect to any of the informatics servers. This was quite confusing for me.

Informatics has a helpful diagram explaining how it works

![VPN Diagram](https://computing.help.inf.ed.ac.uk/sites/default/files/VPN%20onion.png)

- To be able to connect to informatics servers using ssh you need the [Informatics OpenVPN](https://computing.help.inf.ed.ac.uk/openvpn)
- To connect to the rest of the university services you need the [University VPN](https://www.ed.ac.uk/information-services/computing/desktop-personal/vpn)

- [Help page](https://computing.help.inf.ed.ac.uk/vpn) from informatics

