extends Camera
var httpImage
var httpInputRequest
var loader
var on = 0 
var dir = Directory.new()
var isPressed = false
const TMP_FILE = 'user://tmp.jpg'

var pressed = {
	"left":{
		"up":false,
		"down":false
	},
	"right":{
		"up":false,
		"down":false
	}
}

func checkInput():
	
	##Yes I understand there is probably a release o k I know
		if Input.is_action_pressed("turn_left"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y - 1, 0))
			if not pressed.left.up:
				httpInputRequest.request("http://192.168.254.14:5000/pressed?dir=up&side=left")
			pressed.left.up = true
		else:
			if pressed.left.up:
				httpInputRequest.request("http://192.168.254.14:5000/released?dir=up&side=left")
			pressed.left.up = false
			
		if Input.is_action_pressed("turn_right"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y +1, 0))
			if not pressed.right.up:
				httpInputRequest.request("http://192.168.254.14:5000/pressed?dir=up&side=right")
			pressed.right.up = true
		else:
			if pressed.right.up:
				httpInputRequest.request("http://192.168.254.14:5000/released?dir=up&side=right")
			pressed.right.up = false

func _process(delta):
	checkInput()
	if loader:
		var err = loader.poll()
		if err == ERR_FILE_EOF: # load finished
			var resource = loader.get_resource()
			loader = null
			set_image(resource)

func get_image():
	httpImage.set_download_file('user://tmp'+str(on)+'.jpg')
	httpImage.request("http://192.168.254.14:5000/image.jpg")

func image_downloaded(result,response_code,headers,body):
	if result == OK:
		if response_code == 200:
			loader = ResourceLoader.load_interactive('user://tmp'+str(on)+'.jpg')
			
			

func set_image(resource):
	get_node("Quad").get_material_override().set_shader_param("Image",resource)
	
	if dir.file_exists('user://tmp'+str(on-1)+'.jpg'):
		dir.remove('user://tmp'+str(on-1)+'.jpg')
	
	on += 1
	get_image()

func _ready():
	set_process(true)
	#set_process_input(true)
	httpImage = get_node("httpImageRequest")
	httpImage.set_use_threads(true)
	httpImage.connect("request_completed",self,'image_downloaded')
	
	##
	httpInputRequest = get_node("httpInputRequest")
	##could put a return request here
	get_image()