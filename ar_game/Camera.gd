extends Camera
var http
var loader
var on = 0 
var dir = Directory.new()
const TMP_FILE = 'user://tmp.jpg'

func _input(event):
	if event.type == 1:
		if event.is_action("turn_left"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y - 1, 0))
		if event.is_action("turn_right"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y +1, 0))

func _process(delta):
	if loader:
		var err = loader.poll()
		if err == ERR_FILE_EOF: # load finished
			var resource = loader.get_resource()
			loader = null
			set_image(resource)

func get_image():
	http.set_download_file('user://tmp'+str(on)+'.jpg')
	http.request("http://localhost:5000/image.jpg")

func image_downloaded(result,response_code,headers,body):
	if result == OK:
		if response_code == 200:
			loader = ResourceLoader.load_interactive('user://tmp'+str(on)+'.jpg')
			set_process(true)
			

func set_image(resource):
	get_node("Quad").get_material_override().set_shader_param("Image",resource)
	
	if dir.file_exists('user://tmp'+str(on-1)+'.jpg'):
		dir.remove('user://tmp'+str(on-1)+'.jpg')
	
	on += 1
	get_image()

func _ready():
	set_process_input(true)
	http = get_node("HTTPRequest")
	http.set_use_threads(true)
	http.connect("request_completed",self,'image_downloaded')
	
	get_image()