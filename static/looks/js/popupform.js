$(function() {
	// a workaround for a flaw in the demo system (http://dev.jqueryui.com/ticket/4375), ignore!
	//$( "#dialog:ui-dialog" ).dialog( "destroy" );
	
	var category = $( "#item_category" ),
		brand = $( "#product_brand" ),
		pname = $( "#product_name" ),
		url = $( "#product_url" ),
		allFields = $( [] ).add( category ).add( brand ).add( pname ).add( url ),
		tips = $( ".validateTips" );

	function updateTips( t ) {
		tips
			.text( t )
			.addClass( "ui-state-highlight" );
		setTimeout(function() {
			tips.removeClass( "ui-state-highlight", 1500 );
		}, 500 );
	}

	function checkLength( o, n, min, max ) {
		if ( o.val().length > max || o.val().length < min ) {
			o.addClass( "ui-state-error" );
			updateTips( "Length of " + n + " must be between " +
				min + " and " + max + "." );
			return false;
		} else {
			return true;
		}
	}

	function checkRegexp( o, regexp, n ) {
		if ( !( regexp.test( o.val() ) ) ) {
			o.addClass( "ui-state-error" );
			updateTips( n );
			return false;
		} else {
			return true;
		}
	}
	
	function taggingEvents(){
		$('.add_tag').addClass('hidden');
		$('.done_tag').removeClass('hidden');

		$( '#canvas' )
			.click(function(e) {
				var offset = $(this).offset();
				x = Math.round(e.clientX - offset.left);
				y = Math.round(e.clientY - offset.top);
				if (x > 0 && x < parseInt($(this).css('width')) && y > 0 && y < parseInt($(this).css('height'))) {			
					$( '#position' ).val( x +',' + y);
					$( "#div_tag_form" ).dialog( "open" );
				}
	
			});
		function drawSquare(canvas, x, y) {
			var context = $(canvas)[0].getContext('2d');
			context.clearRect(0,0,$(canvas)[0].width,$(canvas)[0].height);
			context.strokeStyle = 'white';
			context.strokeRect(x, y, 100, 100);
	    }
		$( '#canvas' )
			.mousemove(function(e) {
				var xset = false, yset = false;
				var offset = $(this).offset();
				x = e.clientX - offset.left;
				y = e.clientY - offset.top;
				var xMax = parseInt($(this).css('width')) - 50;
				var yMax = parseInt($(this).css('height')) - 50;
				var xMin = 50;
				var yMin = 50;
				var xSquare = 0, ySquare = 0;
				if (x > 0 && x < parseInt($(this).css('width')) && y > 0 && y < parseInt($(this).css('height'))) {			
					if ( x < xMin ){
						xSquare = 0;
						xset = true;
					}
					if ( x > xMax){
						xSquare = xMax - 50;
						xset = true;					
					}
					if ( !xset ) {
						xSquare = x - 50;
					}
					
					if ( y < yMin ){
						ySquare = 0;
						yset = true;
					}
					if ( y > yMax){
						ySquare = yMax - 50;
						yset = true;
					}
					if ( !yset ) {
						ySquare = y - 50;
					}
					//$('#detail_square').css('left', xSquare + 'px');
					//$('#detail_square').css('top', ySquare + 'px');
					//$('#detail_square').removeClass('hidden');
					drawSquare('#canvas', xSquare, ySquare);
				}
				else {
					$('#detail_square').addClass('hidden');
				}
			});
	}
	
	$( "#div_tag_form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 500,
		modal: true,
		buttons: {
			"Add this item": function() {
				var bValid = true;
				allFields.removeClass( "ui-state-error" );

				bValid = category.val() || brand.val() || pname.val() || url.val();
				//bValid = bValid && checkLength( category, "item_category", 3, 16 );
				//bValid = bValid && checkLength( brand, "product_brand", 6, 80 );
				//bValid = bValid && checkLength( pname, "product_name", 5, 16 );
				//bValid = bValid && checkLength( url, "product_url", 5, 16 );

				//bValid = bValid && checkRegexp( url, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
				// From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/

				if ( bValid ) {
					var text = '';
					if (category.val()) {
						text += category.val(); 
					}
					if (brand.val()) {
						if (text) {
							text+=',';
						}
						text += brand.val(); 
					}
					if (pname.val()) {
						if (text) {
							text+=',';
						}
						text += pname.val(); 
					}
					if (url.val()) {
						if (text) {
							text+=',';
						}
						text += url.val(); 
					}
					$( this ).dialog( "close" );
				}
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},		
		close: function() {
			$( "#tag_form" ).submit();
			allFields.val( "" ).removeClass( "ui-state-error" );			
		}
	});

	$( "#add_tag" )
		.button( { label: "Add Tag" } )
		.click(function() {
			taggingEvents();
		});
		
	$( "#done_tag" )
		.button( { label: "Done" })
		.click(function() {
			$('.add_tag').removeClass('hidden');
			$('.done_tag').addClass('hidden');
			location.reload();
		});
});