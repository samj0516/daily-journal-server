import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from entries.request import get_all_entries, get_single_entry, get_entry_by_search, delete_entry, update_entry, create_entry
from instructors.request import get_single_instructor, get_all_instructors, create_instructor, update_instructor, delete_instructor                       
from moods import get_all_moods, get_single_mood, create_mood, delete_mood, update_mood





class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:

            param = resource.split("?")[1] 
            resource = resource.split("?")[0] 
            pair = param.split("=")  
            key = pair[0] 
            value = pair[1] 

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass 
            except ValueError:
                pass  

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)
    
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"

                else:
                    response = f"{get_all_entries()}"

        if resource == "moods":
            if id is not None:
                response = f"{get_single_mood(id)}"

            else:
                response = f"{get_all_moods()}"
        
        if resource == "instructors":
            if id is not None:
                response = f"{get_single_instructor(id)}"

            else:
                response = f"{get_all_instructors()}"
        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "concept" and resource == "entries":
                response = f"{get_entry_by_search(value)}"

        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new item
        new_item = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "entries":
           new_item = create_entry(post_body)
        
        if resource == "moods":
           new_item = create_mood(post_body)
        
        if resource == "instructors":
           new_item = create_instructor(post_body)
        

        # Encode the new animal and send in response
        self.wfile.write(f"{new_item}".encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "entries":
            success = update_entry(id, post_body)
        
        if resource == "moods":
            success = update_mood(id, post_body)
        
        if resource == "instructors":
            success = update_instructor(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

        # Encode the new animal and send in response
        # Not needed because 204 does not return anything
        # self.wfile.write("".encode())


    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)
        
        if resource == "moods":
            delete_mood(id)
        
        if resource == "instructors":
            delete_instructor(id)
        

        # Encode the new animal and send in response
        self.wfile.write("".encode())
# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()