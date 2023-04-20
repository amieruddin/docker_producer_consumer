1. OS : Linux Ubuntu 20.04


2. configure docker

$ sudo apt-get update

	$ sudo apt install docker.io

$ docker --version

$ pip install docker-compose


3. configure rabbitmq

$ sudo chmod 666 /var/run/docker.sock

4. create python environment
$ conda create --name tapway python=3.7
$ conda activate tapway
$ pip install -r requirements

5. run docker-compose
$ docker-compose up --build


6. in postman : create this json data

-method : POST
-URL :  http://localhost.:5000/tapway_task

-pre-request script
let moment = require('moment');
pm.environment.set('currentdate', moment().format(("yyyy-MM-DD HH:mm:ss.SSSSSS")));

-body
{
	"device_id": "Lane10",
	"client_id": "LDP",
	"created_at": "{{currentdate}}",
	"data": {
		"license_id": "PKR1200",
		"preds": [
			{
				"image_frame": "img_based64",
				"prob": 0.18,
				"tags": ["plate_number", "wheel"]
			},
            {
				"image_frame": "img_based64",
				"prob": 0.68,
				"tags": ["plate_number", "wheel"]
			}
		] 
	}
}


