// XML-based Javascript Image Gallery

// Settings
var imageholder_noimagetext = 'Click on an image to view it full size.';
var imageholder_noxmlfile = 'Could not load gallery XML file "';
var imageholder_noxmldata = 'Could not locate the specfied gallery in the XML file "';

// Image Gallery Code
function loadGallery(xmlurl, galleryid) {
	if (window.gallerystatus == undefined) {
		window.gallerystatus = {};
	}
	if (window.galleryxmldata == undefined) {
		window.galleryxmldata = {};
	}
	if (window.galleryerror == undefined) {
		window.galleryerror = {};
	}
	$.ajax({
		type: "GET",
		url: xmlurl,
		dataType: "xml",
		success: function(xml) {
			window.debug = xml;
			var galleryxml = $(xml).find('galleries gallery[id="' + galleryid + '"]');
			if (galleryxml.length < 1) {
				window.gallerystatus[galleryid] = "no_data";
			} else {
				window.gallerystatus[galleryid] = "ok";
				window.galleryxmldata[galleryid] = galleryxml;
			}
			createGallery(xmlurl, galleryid)
		},
		error: function(request, status, error) {
			window.gallerystatus[galleryid] = "no_xml";
			window.galleryerror[galleryid] = [request.status, request.statusText];
			createGallery(xmlurl, galleryid)
		}
	});
};

function createGallery(xmlurl, galleryid) {
	var do_gallery = false;
	// Check outcome of XML retreival
	if (window.gallerystatus[galleryid] == "ok") {
		message = imageholder_noimagetext;
		var do_gallery = true;
	} else if (window.gallerystatus[galleryid] == "no_data") {
		message = imageholder_noxmldata + xmlurl + '"';
	} else if (window.gallerystatus[galleryid] == "no_xml") {
		message = imageholder_noxmlfile + xmlurl + '" Error: ' + window.galleryerror[galleryid][0] + " " + window.galleryerror[galleryid][1];
	} else {
		alert("Unknown error");
	}
	// Load up the actual gallery
	var gallery = $("#igid_" + galleryid);
	if (do_gallery) {
		// Get image selector
		var imageselector = generateImageSelector(galleryid);
	}
	// Get blank image holder
	var imageholder = generateImageHolder_blank(message);
	if (do_gallery) {
		gallery.append(imageselector);
	}
	gallery.append(imageholder);
	imageholder.css("padding-top",((gallery.innerHeight() - imageholder.height())/2) + "px");
};

function switchImage(galleryid, imageid) {
	// Grab the gallery elements
	var gallery = $("#igid_" + galleryid);
	var currentimage = $("#igid_" + galleryid + " div.ig_imageholder");
	var imageselector = $("#igid_" + galleryid + " ul.ig_imageselector");
	// Check if requested image is the current image
	if (imageid == currentimage.attr("id")) { return };
	gallery.addClass("loading_icon");
	// Get data on requested image
	var requestedimage = window.galleryxmldata[galleryid].find('image[id="' + imageid + '"]');

	// Calculate compensation
	// Calculate top and bottom margin compensation
	var margin_top = parseInt(currentimage.css("margin-top").slice(0,currentimage.css("margin-top").length - 2));
	var margin_bottom = parseInt(currentimage.css("margin-bottom").slice(0,currentimage.css("margin-bottom").length - 2));
	var marginpad_height_compensate = margin_top + margin_bottom;

	// Calculate left and right margin compensation
	var margin_left = parseInt(currentimage.css("margin-left").slice(0,currentimage.css("margin-left").length - 2));
	var margin_right = parseInt(currentimage.css("margin-right").slice(0,currentimage.css("margin-right").length - 2));
	var marginpad_width_compensate = margin_left + margin_right;

	// Calculate border compensation
	var border_top = parseInt(gallery.css("border-top-width").slice(0,gallery.css("border-top-width").length - 2));
	var border_bottom = parseInt(gallery.css("border-bottom-width").slice(0,gallery.css("border-bottom-width").length - 2));
	var border_compensate = border_top + border_bottom;

	// Building image request
	var newimagesettings = {
			"id":		requestedimage.attr("id"),
			"src":		requestedimage.attr("src"),
			"height":	requestedimage.attr("height"),
			"width":	requestedimage.attr("width"),
			"alt":		requestedimage.find("alt").text()
	};
	if (requestedimage.children("caption").length == 1) {
		newimagesettings["caption"] = requestedimage.find("caption").text()
	};
	if (requestedimage.attr("link") != undefined) {
		newimagesettings["link"] = requestedimage.attr("link")
	};
	if (requestedimage.children("name").length == 1) {
		newimagesettings["name"] = requestedimage.find("name").text()
	};
	if (requestedimage.children("description").length == 1) {
		newimagesettings["description"] = requestedimage.find("description").text()
	};
	// Get image
	var newimage = generateImageHolder(newimagesettings);
	// Effects
	newimage.hide();
	gallery.append(newimage);

	// Calculate required minimum height and width
	var needed_height = newimage.height() + marginpad_height_compensate;
	var needed_width = newimage.width() + imageselector.width() + marginpad_width_compensate;
	// Calculate vertical alignment
	if (gallery.height() >= needed_height) {
		var nudge_vert = (gallery.height() - newimage.height()) / 2 - border_compensate;
	} else {
		var nudge_vert = (needed_height - newimage.height()) / 2 - border_compensate;
	}

	// Check gallery width and height
	if (gallery.width() < needed_width && gallery.height() < needed_height) {
		// Gallery is too narrow and short to display the image
		gallery.animate({
			"width": needed_width,
			"height": needed_height
		}, "normal");
	} else if (gallery.width() < needed_width) {
		// Gallery is too narrow to display the image
		gallery.animate({
			"width": needed_width
		}, "normal");
	} else if (gallery.height() < needed_height) {
		// Gallery is too short to display the image
		gallery.animate({
			"height": needed_height
		}, "normal");
	}
	// Switch images
	currentimage.fadeOut("slow", function() {
		// Add top padding
		newimage.css("padding-top", nudge_vert);
		currentimage.remove();
		newimage.fadeIn("slow", function() {
			gallery.removeClass("loading_icon");
		});
	});
};

function generateImageSelector(galleryid) {
	var image_selector = $(document.createElement("ul"));
	image_selector.addClass("ig_imageselector");
	window.galleryxmldata[galleryid].find("image").each(function(imgnum) {
		var self = $(this);
		var image_item = $(document.createElement("li"));
		var image = $(document.createElement("img"));
		image.attr({
			"src": self.attr("src"),
			"alt": self.find("alt").text()
		});
		if (self.children("caption").length == 1) { image.attr("title", self.find("caption").text()); }
		image.click(function() { switchImage(galleryid, self.attr("id")); });
		image_item.append(image);
		image_selector.append(image_item);
	});
	return image_selector;
};

function generateImageHolder(settings) {
	var holder = $("<div></div>").attr({
		"class":	'ig_imageholder',
		"id":		settings["id"]
	});
	var img = $('<img>').attr({
		"src":		settings["src"],
		"height":	settings["height"],
		"width":	settings["width"],
		"alt":		settings["alt"]
	});
	if ("caption" in settings) { img.attr("title", settings["caption"]); }
	if ("link" in settings) {
		$("<a></a>").attr("href", settings["link"]).append(img).appendTo(holder);
	} else {
		holder.append(img);
	}
	if ("name" in settings) { $('<span></span>').text(settings["name"]).addClass("ig_imagename").appendTo(holder); }
	if ("description" in settings) { $("<p></p>").text(settings["description"]).addClass("ig_imagedesc").appendTo(holder); }
	return holder;
};

function generateImageHolder_blank(message) {
	holder = $(document.createElement("div"));
	holder.addClass("ig_imageholder");
	if (message != imageholder_noimagetext) {
		holder.addClass("ig_msgholder");
	}
	var message_span = $(document.createElement("span"));
	message_span.addClass("ig_msg").text(message);
	holder.append(message_span);
	return holder
};
