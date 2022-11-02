# Discord-Bot-Tero-
Currently this bot has only options to give temporary a role to an user. But it will be expanded in the future

## Commands:
- !addrole user role duration
- !removerole user role 

## Duration optinos: 

m - minute  
h - hour  
d - day   
M - month   
y - year  

## Examples of using commands: 

!addrole DaJMaN vip 44d 

!removerole DaJMaN vip 

#

prefix can be change by changing the string in this line: client = commands.Bot(command_prefix='!')

New string will be new prefix 

## PLC communication script: 
Enables to read digital tags of siemens PLCs and writes value of digital tags into PLCs memory

Usage: 

!writePLC tag value

Tag must be an existing tag in PLCs memory

Value must be an boolean, you can write it like this: true, false, 0, 1


Made for fun 
