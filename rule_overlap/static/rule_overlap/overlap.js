function openModal() {
	document.getElementById('modal').style.display = 'block';
	document.getElementById('fade').style.display = 'block';
}

function closeModal() {
	document.getElementById('modal').style.display = 'none';
	document.getElementById('fade').style.display = 'none';
}

var findRuleOverlaps = function(e){
  var prodattr = $('#prodattr').val();

  if (prodattr === null)
    return;

    runOverlap(prodattr);
}

var runOverlap = function(productName){
if ($('#prodattr').val() == '') {
    alert("Please enter a target product attribute name.");
  return false;
}
  var myInput = new Object();
  myInput['prodattr'] = $('#prodattr').val();
  myInput['ruleattr'] = $('#cat_codes').val();

  openModal();
  $.ajax({
          type: 'POST',
          contentType: 'application/json; charset=utf-8',
          dataType: 'json',
          url: '/rule_overlap/find',
          timeout: 0,
          data: JSON.stringify(myInput),
        }).done(function(data) {
          createTables(data)
        }).fail(function(j,s,t) {
          alert(j.responseText)
          alert(s)
          alert(t)
        });
  return false;
}

var createTables = function(data) {
  closeModal();
  $("#results").empty();
  // alert(data['attr_rule_map']);
	if (data['attr_rule_map'] == '') {
      $("#results").append('<tr><th><i>No overlaps found.</i></th></tr>');
	}
	else {
      $("#results").append('<tr><th>Overlapping Rules</th><th>Overlapping Value</th><th>No. Item(s)</th></tr><tr><th></th><th></th><th></th><td>' +data['attr_rule_map']+'</td></tr>');
	}
}
