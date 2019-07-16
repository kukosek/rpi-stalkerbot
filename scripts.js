function containsOnly(array1, array2){
      return array2.every(elem => array1.includes(elem))
}
    function post(data) {
        $.ajax({
            type: "POST",
            url: window.location.href,
            data: data,
            dataType: "text",
            start_time: new Date().getTime(),
            success: function(resultData) {
                console.log("sended")
                $("#status").text('Last request completed succesfully in '+(new Date().getTime() - this.start_time)+' ms');
                $("#status").css('color', 'green');
            },
            error: function(resultError) {
                console.log("not sended")
                $("#status").text('Last request completed with error in '+(new Date().getTime() - this.start_time)+' ms');
                $("#status").css('color', 'red');
            }   
        });
        $("#status").text('Sending request...');
        $("#status").css('color', 'black');
    }
    
    function shutdown(reboot){
        if (confirm("Do you really wanna do that maan?")){
            if (prompt("Enthe the passphrase to confirm ya not a troll xd")=="no boi"){
                post({"action":"shutdown","param":reboot});
            }        
        }
        
    }

    function camRotation(angle){
        console.log(angle);
        if (angle==0 || angle==90 || angle==180 || angle==270){
            post({"action":"camRotation","param":angle});
        }
    }

    function reloadFiles(){
        $.ajax({
            type: "GET",
            url: window.location.href.replace('index.html','files.txt'),
            start_time: new Date().getTime(),
            success: function(resultData) {
                console.log("sended")
                $("#status").text('Last request completed succesfully in '+(new Date().getTime() - this.start_time)+' ms');
                $("#status").css('color', 'green');
                files=resultData.split(';');
                $('select[name=fileSelect]').empty();
                files.forEach(function(file) {
                    $('select[name=fileSelect]').append('<option value="'+file+'">'+file+'</option>');
                });
            },
            error: function(resultError) {
                console.log("not sended")
                $("#status").text('Last request completed with error in '+(new Date().getTime() - this.start_time)+' ms');
                $("#status").css('color', 'red');
            }
        });
        $("#status").text('Sending request...');
        $("#status").css('color', 'black');
        
    }
    

    function keyboardCheck(){
        if(moveKeyPressedState==false || !moveKeycodes.includes(keycode)){
            moveKeycodes.push(keycode);
            
            
            switch(true){
                case containsOnly([38],moveKeycodes): //right
                    post({"action":"move","param":"forward"});
                    moveKeyPressedState=true;
                    break;
                case containsOnly([40],moveKeycodes): //down
                    post({"action":"move","param":"backwards"});
                    moveKeyPressedState=true;
                    break;

                case containsOnly([37],moveKeycodes): //left
                    post({"action":"move","param":"left"});
                    moveKeyPressedState=true;
                    break;
                case containsOnly([37,38],moveKeycodes): //left and up
                    post({"action":"move","param":"forwardLeft"}); //slowly
                    moveKeyPressedState=true;
                    break;

                case containsOnly([39],moveKeycodes): //right
                    post({"action":"move","param":"right"});
                    moveKeyPressedState=true;
                    break;
                case containsOnly([38,39],moveKeycodes): //right and up
                    post({"action":"move","param":"forwardRight"}); //slowly
                    moveKeyPressedState=true;
                    break;
		    }
        }
        if(camKeyPressedState==false || !camKeycodes.includes(keycode)){
            camKeycodes.push(keycode);
            console.debug(camKeycodes)
		    switch(true){
                case containsOnly([87],camKeycodes): //w
                    //cameraup
				    post({"action":"camMove","param":"up"});
                    camKeyPressedState=true;
                    break;
                case containsOnly([83],camKeycodes): //s
                    //cameradown
				    post({"action":"camMove","param":"down"});
                    camKeyPressedState=true;
                    break;
                case containsOnly([65],camKeycodes): //a
                    //cameraleft
				    post({"action":"camMove","param":"left"});
                    camKeyPressedState=true;
                    break;
			    case containsOnly([65,87],camKeycodes): //a and w
                    //cameraleftup
				    post({"action":"camMove","param":"leftup"});
                    camKeyPressedState=true;
                    break;

			    case containsOnly([65,83],camKeycodes): //a and s
                    //cameraleftdown
				    post({"action":"camMove","param":"leftdown"});
                    camKeyPressedState=true;
                    break;
                case containsOnly([68],camKeycodes): //d
                    //cameraright
				    post({"action":"camMove","param":"right"});
                    camKeyPressedState=true;
                    break;
			    case containsOnly([68,87],camKeycodes): //d and w
                    //camerarightup
				    post({"action":"camMove","param":"rightup"});
                    camKeyPressedState=true;
                    break;

			    case containsOnly([68,83],camKeycodes): //d and s
                    //camerarightdown
				    post({"action":"camMove","param":"rightdown"});
                    camKeyPressedState=true;
                    break;
                
        	    }
            if (keycode==67){
			    post({"action":"camSetPos","param":"0,0"});		
		    }
        }
    }

    var moveKeycodes=[]
    var camKeycodes=[]
    var moveKeyPressedState=false;
    var camKeyPressedState=false
    var prevKeycode=1;
    var keycode=0;
    window.addEventListener('keydown', function (e) {
        keycode=e.keyCode;
        keyboardCheck();
        prevKeycode=keycode;
    })
    window.addEventListener('keyup', function (e) {
        keycode=e.keyCode;
        moveKeycodes = moveKeycodes.filter(function(element) {
                return element !== keycode;
            })
        camKeycodes = camKeycodes.filter(function(element) {
                    return element !== keycode;
                })
        if (moveKeyPressedState){
            if (containsOnly([keycode],moveKeycodes)){
                moveKeycodes=[];
                moveKeyPressedState=false;
                post({"action":"move","param":"stop"});
            }else if (moveKeycodes.includes(keycode)){
                moveKeycodes = moveKeycodes.filter(function(element) {
                    return element !== keycode;
                })
                moveKeyPressedState=false;
                keyboardCheck();     
            }    
        }

        if (camKeyPressedState){
            if (containsOnly([keycode],camKeycodes)){
                camKeycodes=[]
                camKeyPressedState=false;
                post({"action":"camMove","param":"stop"});
            }else if (camKeycodes.includes(keycode)){
                camKeycodes = camKeycodes.filter(function(element) {
                    return element !== keycode;
                })
                camKeyPressedState=false;
                keyboardCheck();     
            }        
        }
    })
