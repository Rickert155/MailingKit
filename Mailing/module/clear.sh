sudo apt purge apache2 php8.1 zip mailutils opendkim opendkim-tools ipython3 -y
sudo apt purge install postfix dovecot-imapd dovecot-pop3d -y 
cd ~ && rm -rf Mailing
sudo rm -r /etc/opendkim /etc/opendkim.conf /etc/postfix
userdel sin 
sudo apt autoremove -y
