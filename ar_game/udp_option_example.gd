extends Node
var socket

func _process(delta):
	#Client update
	var f = File.new()
	while (socket.get_available_packet_count() > 0):
		var packet = socket.get_packet()
		if(f.open( "res://testImage.jpg", File.WRITE )==0):
			f.store_buffer(packet)
			f.close()
			
			var img = ImageTexture.new()
			img.load( "res://testImage.jpg" )
			get_node("Sprite").set_texture(img)
			
func _ready():
	socket = PacketPeerUDP.new()
	socket.set_send_address("localhost", 9998)
	if (socket.listen(9999) != OK):
		print("Error listening on port ", '9999')
		return
	else:
		print("Listening on port ", '9999')
	set_process(true)