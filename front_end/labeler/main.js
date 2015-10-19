$(document).ready(function(){
	//temporary array to store sol data
	var sols = [];

	//array of image objects
	var images = [];

	var features = [];

	//index of the current image the user is viewing
	var currImage = 0;

	//user is submitting labels for current image
	$("#doneButton").click(function(){
		//add user input to features obj
		var feature = new Object();

		feature.imagePath = images[currImage].path;
		feature.interesting = $('input[name="interesting"]:checked').length > 0;
		feature.crater = $('input[name="crater"]:checked').length > 0;

		features.push(feature);

		currImage++;
		nextImage();
	});

	function generateCSV(){
		//init csv data with headers
		var csvData = [['imagePath','interesting','crater']];

		//add features to csv data
		for (var i = 0; i < features.length; i++){ 
		    csvData.push([features[i].imagePath, features[i].interesting, features[i].crater]);
		}

		var csvRows = [];

		for(var i = 0; i < csvData.length; i++){
		    csvRows.push(csvData[i].join(','));
		}

		var csvString = csvRows.join("%0A");
		var a         = document.createElement('a');
		a.href        = 'data:attachment/csv,' + csvString;
		a.target      = '_blank';
		a.download    = 'myFile.csv';

		document.body.appendChild(a);
		a.click();
	}

	//executes when all of the image paths have been stored
	//AND when user presses done button
	function nextImage(){
		//make sure we don't go oob for images array
		if (currImage == images.length) {
			alert("all done :)");

			generateCSV();
		} else {
			//reset checkboxes (turn them all off)
		    $('input:checkbox').removeAttr('checked');  

			//update content
			$("#currImage").html("<img src='" + images[currImage].path + "'/>");
			$("#currImageSol").html(images[currImage].sol);
			$("#currImageName").html(images[currImage].name);
			$("#currImageNum").html(currImage);
		}
	}

	//finds all of the images in the root URL and subdirs
	function init(){
		var rootURL = "http://localhost:8000/images/";
		$.ajax({
		  url: rootURL,
		  success: function(data){
		     $(data).find("li > a").each(function(){
		        if ($(this).attr("href").indexOf("sol") != -1){
		        	var sol = $(this).attr("href");
		        	
		        	//chop off '/' from sol
		        	sol = sol.substring(0, sol.length - 1);

		        	sols.push(sol);
		        }
		     });

		     for (var i = 0; i < sols.length; i++){
		     	(function(i){
			   		$.ajax({
						  url: rootURL + sols[i],
						  success: function(data){
						     $(data).find("li > a").each(function(){
						        if ($(this).attr("href").indexOf("image") != -1){
						        	var image = new Object();

						        	image.name = $(this).attr("href");
						        	image.sol = sols[i];
						        	image.path = rootURL + sols[i] + "/" + $(this).attr("href");

						        	images.push(image);
						        }
						     });

						     //when we have pulled all of the images, we are ready to display them to the client
						     if (i == sols.length - 1){
						     	nextImage();
						     }
						  }
					});
			    })(i);
		     }
		  }
		});
	}

	init();
});