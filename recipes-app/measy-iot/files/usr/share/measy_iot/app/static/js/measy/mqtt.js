$('#server_form').validate({
    submitHandler: function(form) {
    // some other code
    // maybe disabling submit button then:
    alert('server_form submitted!');
  },
  rules: {
    mq_clientid_input: 'required',
    mq_port_input: 'required',
    mq_host_input: {
      required: true,
      minlength: 2
    }
  },
  messages: {
    mq_clientid_input: '{{ _("CONNECT")}}',
    mq_port_input: 'Please enter your lastname',
    mq_host_input: {
      required: 'Please enter a username',
      minlength: 'Your username must consist of at least 2 characters'
    }
  },
  errorElement: 'em',
  errorPlacement: function errorPlacement(error, element) {
    error.addClass('invalid-feedback');

    if (element.prop('type') === 'checkbox') {
      error.insertAfter(element.parent('label'));
    } else {
      error.insertAfter(element);
    }
  },
  // eslint-disable-next-line object-shorthand
  highlight: function highlight(element) {
    $(element).addClass('is-invalid').removeClass('is-valid');
  },
  // eslint-disable-next-line object-shorthand
  unhighlight: function unhighlight(element) {
    $(element).addClass('is-valid').removeClass('is-invalid');
  }
});

$('#sub_form').validate({
    submitHandler: function(form) {
    // some other code
    // maybe disabling submit button then:
    alert('sub_form submitted!');
  },
  rules: {
    mq_subtopic_input: 'required',
  },
  messages: {
    mq_subtopic_input: '{{ _("CONNECT")}}',
  },
  errorElement: 'em',
  errorPlacement: function errorPlacement(error, element) {
    error.addClass('invalid-feedback');

    if (element.prop('type') === 'checkbox') {
      error.insertAfter(element.parent('label'));
    } else {
      error.insertAfter(element);
    }
  },
  // eslint-disable-next-line object-shorthand
  highlight: function highlight(element) {
    $(element).addClass('is-invalid').removeClass('is-valid');
  },
  // eslint-disable-next-line object-shorthand
  unhighlight: function unhighlight(element) {
    $(element).addClass('is-valid').removeClass('is-invalid');
  }
});

$('#pub_form').validate({
    submitHandler: function(form) {
    // some other code
    // maybe disabling submit button then:
    alert('pub_form submitted!');
  },
  rules: {
    mq_pub_topic: 'required',
    mq_pub_message: 'required'
  },
  messages: {
    mq_pub_topic: '{{ _("CONNECT")}}',
    mq_pub_message: '{{ _("CONNECT") }}'
  },
  errorElement: 'em',
  errorPlacement: function errorPlacement(error, element) {
    error.addClass('invalid-feedback');

    if (element.prop('type') === 'checkbox') {
      error.insertAfter(element.parent('label'));
    } else {
      error.insertAfter(element);
    }
  },
  // eslint-disable-next-line object-shorthand
  highlight: function highlight(element) {
    $(element).addClass('is-invalid').removeClass('is-valid');
  },
  // eslint-disable-next-line object-shorthand
  unhighlight: function unhighlight(element) {
    $(element).addClass('is-valid').removeClass('is-invalid');
  }
});
    // <script type="text/javascript" charset="utf-8">
    $(document).ready(function() {
            var mqtt_connected = "{{appbuilder.app.mqtt_connected}}";
            console.log("mqtt_connected:::" + mqtt_connected);
            if(mqtt_connected === "connected"){
                $("#mq_switch").attr("checked", "checked");
            }
            else
            {
                $("#mq_switch").removeAttr("checked")
            }
            $("#mq_switch").click(function () {
                  console.log("checkbox click");
                  return false;
            });

            $("#server_form").submit(function (){
                 console.log("connecting server");
                    var mq_clientid = $("#mq_clientid_input").val();
                    var mq_host = $("#mq_host_input").val();
                    var mq_port = $("#mq_port_input").val();
                    var mq_qos = $("#mq_qos_select").val();
                    var mq_retain = $("#mq_retain_radio").val();

                    var data = {
                        data: JSON.stringify({
                            'mq_clientid': mq_clientid,
                            'mq_host': mq_host,
                            'mq_port': mq_port,
                            'mq_qos': mq_qos,
                            'mq_retain':mq_retain
                        }),
                    };
                    //
                    // $.ajax({
                    //     url:'/measy/mqtt',
                    //     type:'POST',
                    //     data:data,
                    //     dataType:'json',
                    //     success:function (res) {
                    //         mq_switch.attr("checked", true);
                    //     },
                    //     error:function (res) {
                    //         mq_switch.attr("checked", false);
                    //         console.log(res);
                    //         console.log(1);
                    //     }
                    // });
                    if(mqtt_connected === "disconnected") {
                        socket.emit('mq_connect', data);
                    }
            });

            $("#mq_disconnect_btn").click(function () {
                socket.emit('mq_disconnect');
            });

            $("#message_list").on("click", "li .icon-close", function () {
                $(this).closest('li').remove();
            });
            $("#mq_pub_btn").on("click",  function(){
                var mq_pub_topic = $("#mq_pub_topic").val();
                var mq_pub_message = $("#mq_pub_msg").val();
                var mq_pub_qos = $("#mq_pub_qos").val();
                    var data = {
                        data:JSON.stringify({
                            'mq_topic': mq_pub_topic,
                            'mq_message': mq_pub_message,
                            'mq_qos': mq_pub_qos,
                        }),
                    };

                    socket.emit("mq_publish", data);
            });

            $("#mq_sub_btn").on("click", function(){
                var mq_sub_topic = $("#mq_subtopic_input").val();
                    var data = {
                        data: JSON.stringify({
                            'mq_topic': mq_sub_topic,
                        }),
                    };
                socket.emit("mq_subscribe", data);
            });

            $("#mq_unsub_btn").on("click", function(){
                var mq_sub_topic = $("#mq_subtopic_input").val();
                    var data = {
                        data:JSON.stringify({
                            'mq_topic': mq_sub_topic,
                        }),
                    };
                $("#sub_form").valid();
                socket.emit("mq_unsubscribe", data);
            });

            $("#clear_message").click(function () {
                var ul = document.getElementById("message_list");
                while(ul.hasChildNodes()){
                    ul.removeChild(ul.firstChild);
                }
            });



    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data to the client. The data is then displayed
    // in different section of the page.
    socket.on('mqtt_connection', function (msg) {
                var status = msg.status;
                if(status === "connected"){
                    $("#mq_switch").attr("checked", true);
                }
                else
                {
                    $("#mq_switch").removeAttr("checked")
                }
            });

    socket.on('mqtt_message', function (msg) {
                var  list_item =
                    "<li class='list-group-item list-group-item-action flex-column align-items-start' style='padding: 0.75rem;'>"+
                    "<div class='d-flex w-100 justify-content-between'>" +
                    "   <h3 class='uppercase bold'>" +
                    "       <p>"+msg.count+"</p>" +
                    "   </h3> " +
                    "   <span class='list-icon-container'> " +
                    "       <a href='javascript:;'> " +
                    "           <i class='icon-close'></i> " +
                    "       </a> " +
                    "   </span> " +
                    "</div>"+
                    "<div class='d-flex w-100 justify-content-between'>" +
                    "   <p>"+msg.data+"</p>" +
                    "   <span class='list-datetime'>"+ new Date().Format("hh:mm:ss") +
                    "   <br/>"+ new Date().Format("yyyy-MM-dd") +" </span>" +
                    "</div>" +
                    "</li>";

                $('#message_list').append(list_item);
            });
 });