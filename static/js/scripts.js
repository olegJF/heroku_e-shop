$(document).ready(function() {
	$('.cart-container').on('click', 'hover', function(e){
		e.preventDefault();
		$('.cart-items').removeClass('hidden');
	

	})
	$('#cart').mouseover( function(){
		$('.cart-items').removeClass('hidden');
	})
	
	$('#cart').mouseout( function(){
		$('.cart-items').addClass('hidden');
	})
});