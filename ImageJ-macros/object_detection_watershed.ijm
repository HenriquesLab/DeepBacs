//-------------------------------------------------------------------------
// Date: October-2021
// Citation: 
// Authors: 
// C. Spahn, R. F. Laine, P. Matos Pereira, L. von Chamier, M.ia Conduit, 
// E. Gómez-de-Mariscal, M. Gomes de Pinho, G. Jacquemet, S. Holden, 
// M. Heilemann, R. Henriques
//
// Title: 
// DeepBacs: Bacterial image analysis usingopen-source deep learning approaches
// URL: 
// 		https://github.com/HenriquesLab/DeepBacs
//-------------------------------------------------------------------------
//  ImageJ macro to detect each independent object using marker-controlled watershed
//  segmentation. It expects a mask with two types of labels: the object and 
//  its boundary. It erodes the interior part of the object to crate the 
//  landmarks and runs watershed with it.
//
//  REQUIREMENTS:
//	- Mask with two labels (values 0 = background, 1 = object, 2 = boundary
//  - MorpholibJ plugin
//
//  PATH: the path were you store a folder called predictions with the masks
//  input_folder: the predictions folder. If it has a differente name, please change it
//  new_folder_seg: the name of the new folder containing the instances
//-------------------------------------------------------------------------


PATH = "/Users/esti/Documents/DeepBact/UNet-training/ECOLI-semantic-03/"
input_folder = "predictions/"
new_folder_seg = "instances/"


files = getFileList(PATH + input_folder);
print(files.length+" images in the directory " + PATH);

if (!File.exists(PATH + new_folder_seg)){
  	File.makeDirectory(PATH + new_folder_seg);
  	if (!File.exists(PATH + new_folder_seg)){
  		exit("Unable to create a directory for masks. Check User permissions.");
  	}
  }
  
// Process each image with the trained model and save the results.
for (i=0; i<files.length; i++) {
	// avoid any subfolder
	if (endsWith(files[i], ".tif")){
		// store the name of the image to save the results
		image_name = split(files[i], ".");
		image_name = image_name[0];  

		// open the image and create a mask for all the segmemted labels
		open(PATH + input_folder + files[i]);	
		
		setThreshold(1, 255);
		run("Convert to Mask");
		run("Grays");
		rename("mask");

		// open the image again to get the markers
		// (inner aprt of the object)
		open(PATH + input_folder + files[i]);	
		setThreshold(1, 1);
		run("Convert to Mask");
		run("Grays");
		rename("markers");

		// Erosion on the markers to ensure that objects are disconnected 
		// (check out the size of the radius for thin objects)
		selectWindow("markers");
		run("Morphological Filters", "operation=Erosion element=Disk radius=2");

		// Runn marker controlled watershed segmentation (MorpholibJ plugin)
		run("Marker-controlled Watershed", "input=mask marker=markers-Erosion mask=mask binary calculate use");

		// Choose a colorful LUT
		selectWindow("mask-watershed");
		run("Set Label Map", "colormap=[Golden angle] background=Black shuffle");	

		// save the result as 8 bits (for high density better chose 16 bits)
		selectWindow("mask-watershed");
		//run("16-bit");
		run("8-bit");
		saveAs("Tiff", PATH + new_folder_seg+image_name+".tif");
		run("Close All");		
		}
	}