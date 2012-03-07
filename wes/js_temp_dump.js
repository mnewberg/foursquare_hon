var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-29130143-1']);
  _gaq.push(['_setDomainName', 'tryfourplay.com']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();


	
	        jQuery(window).ready(function(){  
	            jQuery("#btnInit").click(initiate_geolocation);  
	        });
	                jQuery(window).ready(function(){  
	            jQuery("#btnInit2").click(initiate_geolocation_male);  
	        });  


	        function initiate_geolocation() {  
	            navigator.geolocation.getCurrentPosition(handle_geolocation_query,handle_errors);  
	        }


	        function initiate_geolocation_male() {  
	            navigator.geolocation.getCurrentPosition(handle_geolocation_query_male,handle_errors);  
	        }  


	        function handle_errors(error)  
	        {  
	            switch(error.code)  
	            {  
	                case error.PERMISSION_DENIED: alert("you did not share geolocation data!");  
	                break;  

	                case error.POSITION_UNAVAILABLE: alert("could not detect current position");  
	                break;  

	                case error.TIMEOUT: alert("retrieving position timed out");  
	                break;  

	                default: alert("unknown error");  
	                break;  
	            }  
	        }
					
	

	                function handle_geolocation_query(position){
	                var lat=position.coords.latitude
	                var lon=position.coords.longitude 
				

	                  	$('input[name=lat]').val(lat);
						$('input[name=lon]').val(lon);
						$('input[name=gender]').val('female')
						$('#MyForm').submit();  
                $.mobile.loadingMessage = "Loading up lots of chicks... please be patient!";

					}

					function handle_geolocation_query_male(position){					
		                var lat=position.coords.latitude
		                var lon=position.coords.longitude 


	                  	$('input[name=lat]').val(lat);
						$('input[name=lon]').val(lon);
						$('input[name=gender]').val('male')
						$('#MyForm').submit();
		$.mobile.loadingMessage = "Loading up lots of dudes... please be patient!";
  

					}


jQuery(window).ready(function(){
    jQuery("#person1").live("click",function(){
                $.ajax({
                type: "POST",
                url: "/rating/",
                data:{
                                chosen_id:$(".ui-page-active .id_val").val(),
                                pic_id2:$(".ui-page-active .id_val2").val(),
                                venue_id:$(".ui-page-active .venue1").val(),
                                venue_id2:$(".ui-page-active .venue2").val(),
                                csrfmiddlewaretoken:$("[name='csrfmiddlewaretok\
en']").val()
                          }
		});
})});

jQuery(window).ready(function(){
    jQuery("#person2").live("click",function(){
                $.ajax({
		type: "POST",
                url: "/rating/",
                data:{
                                chosen_id:$(".ui-page-active .id_val2").val(),
                                pic_id2:$(".ui-page-active .id_val").val(),
                                venue_id2:$(".ui-page-active .venue2").val(),
                                venue_id:$(".ui-page-active .venue1").val(),
		                        csrfmiddlewaretoken:$("[name='csrfmiddlewaretok\
en']").val()
                          }
                });
})});