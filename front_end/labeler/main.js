$(document).ready(function(){
	//temporary array to store sol data
	var sols = [];

	//array of image objects
	var images = [];

	var features = [];

	//index of the current image the user is viewing
	var currImage = 0;

	var classifications = [
		"interesting",
		"crater",
		"rocks",
		"arm_visible",
		"wheels",
		"rought_terrain",
		"sand_grooves",
		"hills",
		"sun_stars_moon",
		"sky",
		"gravel",
		"tire_tracks",
		"photo_artifact",
		"dirty_camera",
		"rover_shadow",
		"dusty_sky",
		"dark",
		"soft_sand"
	];

	//user is submitting labels for current image
	$("#doneButton").click(function(){
		//add user input to features obj
		var feature = new Object();

		feature.imagePath = images[currImage].path;

		for (var i = 0; i < classifications.length; i++){
			feature[classifications[i]] = $('input[name=' + classifications[i] + ']:checked').length > 0;
		}

		features.push(feature);

		currImage++;
		nextImage();
	});

	function generateCSV(){
		//init csv data with headers
		var csvData = [['imagePath']];

		//add classifications to headers
		for (var i = 0; i < classifications.length; i++){
			csvData.push(classifications[i]);
		}

		//add features to csv data
		for (var i = 0; i < features.length; i++){ 
			var tmpRow = [];

			tmpRow.push(features[i].imagePath);

			for (var i = 0; i < classifications.length; i++){
				tmpRow.push(features[i][classifications[i]]);
			}

			csvData.push(tmpRow);
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

	//adds all classifications to HTML
	function initHTML(){
		for (var i = 0; i < classifications.length; i++){
			var tmpHTML = "<input type='checkbox' name='" + classifications[i] + "' value='" + classifications[i] + "'> " + classifications[i] + "<br>";

			$("#doneButton").prepend();
		}
	}

	//finds all of the images in the root URL and subdirs
	function initData(){
		var rootURL = "images/";
		$.ajax({
		  url: rootURL,
		  success: function(data){
		      console.log(data);
		     $(data).find("td > a").each(function(){
		        if ($(this).attr("href").indexOf("SOL") != -1){
			    
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
						      console.log(data);
						     $(data).find("td > a").each(function(){
						        if ($(this).attr("href").indexOf(".gif") != -1){
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

	initHTML();
	initData();
});
