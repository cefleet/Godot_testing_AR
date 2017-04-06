extends Camera
var socket
var httpImage
var httpInputRequest
var loader
var on = 0 
var dir = Directory.new()
var isPressed = false
const TMP_FILE = 'res://tmp.jpg'

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
				httpInputRequest.request("http://192.168.0.18:5000/pressed?dir=up&side=left")
			pressed.left.up = true
		else:
			if pressed.left.up:
				httpInputRequest.request("http://192.168.0.18:5000/released?dir=up&side=left")
			pressed.left.up = false
			
		if Input.is_action_pressed("turn_right"):
			set_rotation_deg(Vector3(0,get_rotation_deg().y +1, 0))
			if not pressed.right.up:
				httpInputRequest.request("http://192.168.0.18:5000/pressed?dir=up&side=right")
			pressed.right.up = true
		else:
			if pressed.right.up:
				httpInputRequest.request("http://192.168.0.18:5000/released?dir=up&side=right")
			pressed.right.up = false

func _process(delta):
	checkInput()
	if loader:
		print('there is a loader')
		var err = loader.poll()
		if err == ERR_FILE_EOF: # load finished
			print('File has ended')
			var resource = loader.get_resource()
			loader = null
			set_image(resource)
			
	var f = File.new()
	while (socket.get_available_packet_count() > 0):
		print('there are packets avalible')
		var packet = socket.get_packet()
		if(f.open( TMP_FILE, File.WRITE )==0):
			f.store_buffer(packet)
			f.close()
			loader = ResourceLoader.load_interactive(TMP_FILE)			

func set_image(resource):
	get_node("Quad").get_material_override().set_shader_param("Image",resource)
	
	#if dir.file_exists('user://tmp'+str(on-1)+'.jpg'):
	#	dir.remove('user://tmp'+str(on-1)+'.jpg')
	
	on += 1
	
func _ready():
	socket = PacketPeerUDP.new()
	socket.set_send_address("192.168.0.10", 9998)
	if (socket.listen(9999) != OK):
		print("Error listening on port ", '9999')
		return
	else:
		print("Listening on port ", '9999')
	loader = ResourceLoader.load_interactive("res://img.jpg")
	httpInputRequest = get_node("httpInputRequest")
	set_process(true)