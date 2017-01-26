extends Camera
var texture = ImageTexture.new()
var on = 0
var image = null
var http

const TMP_FILE = 'user://tmp.png'

func _input(event):
	if event.type == 1:
		if event.is_action("turn_left"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y - 1, 0))
		if event.is_action("turn_right"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y +1, 0))


func _fixed_process(delta):
	image = get_node("Viewport").get_screen_capture()
	#texture.set_data(image)
	get_node("Quad").get_material_override().set_shader_param("Image",load("res://icon.png"))
	
func _ready():
	
	texture.create(400,230,3)
	set_process_input(true)
	#set_fixed_process(true)
	
		
	http = get_node("HTTPRequest")
	http.set_use_threads(true)
	http.connect("request_completed",self,'image_downloaded')	
	get_image()

func get_image():
	http.set_download_file('user://tmp'+str(on)+'.png')
	http.request("http://localhost:8081/image.png")


func image_downloaded(result,response_code,headers,body):
	if result == OK:
		if response_code == 200:
			set_image()
			
#look at this
#https://www.youtube.com/watch?v=cGJ978TSmbs

func set_image():
	get_node("Quad").get_material_override().set_shader_param("Image",load('user://tmp'+str(on)+'.png'))
	#this makes up to 30 images... IT still freezes
	#the webserver saves the image to the the root image.png.. but it needs to not save the file instead just 
	#send the raw image data
	if on == 30:
		on = 0
	else:
		on = on+1
	get_image()
	