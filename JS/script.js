var row_id = document.getElementById("item_table").rows.length;
console.log(row_id);

$(document).ready(function(){

//add row
$('.item_bar').focus();


//remove row
 $(document).on('click', '.remove',function(){
  $(this).closest('tr').remove();
  totalamount();
 });

//prevent enter to work on the page
 $(document).keypress(function(event){
     if (event.which == '13') {
       event.preventDefault();
     }
 });

//insert data to database
 $('#insert_form').on('submit', function(event){

  event.preventDefault();
  var error = '';
  $('.item_bar').each(function(){
   var count = 1;
   if($(this).val() == '')
   {
    error += "<p>Enter Item Name at "+count+" Row</p>";
    return false;
   }
   count = count + 1;
  });

  $('.item_quantity').each(function(){
   var count = 1;
   if($(this).val() == '')
   {
    error += "<p>Enter Item Quantity at "+count+" Row</p>";
    return false;
   }
   count = count + 1;
  });


  if(error == '')
  {
   $.ajax({
    url:"/insert",
    method:"POST",
    data:$(this).serialize(),
    success:function(data)
    {
     if(data.data == 'ok')
     {
      $('#item_table').find("input").val('');
      $('#item_table').find("tr:gt(1)").remove();
      $('#total_amount').val('');
      row_id = 2;
      $('#error').html('<div class="alert alert-success">Item Details Saved</div>');
     }
    }
   });
  }
  else
  {
   $('#error').html('<div class="alert alert-danger">'+error+'</div>');
  }
 });

});
