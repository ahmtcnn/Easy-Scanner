for method in OPTIONS GET HEAD POST PUT DELETE TRACE CONNECT ; do 
    echo -e "\n\nTrying $method\n\n" 
    echo -e "$method / HTTP/1.1\nHost: server-hostname\nConnection: close\n\n" | nc bekchy.com 80 | head 
    sleep 2
done