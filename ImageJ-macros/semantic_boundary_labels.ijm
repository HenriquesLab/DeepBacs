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
//  ImageJ macro to calculate the boundary of each object in the image and 
//  create a mask that has two labels: 1 = object, 2 = object boundary. 
//
//  REQUIREMENTS:
//	- Instance segmentations of your objects: the binary mask of each object has a unique label in the image
//  - MorpholibJ plugin
//
//  PATH: the path were you store a folder called target with the instance segmentation
//  input_folder: the target folder. If it has a differente name, please change it
//  new_folder_seg: the name of the new folder containing the semantic segmentation
//-------------------------------------------------------------------------

PATH = "/Users/esti/Documents/DeepBact/Segmentation_Mixed/Bsubtilis/training/"
input_folder = "target/"
new_folder_seg = "semantic_segmentation/"

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

		// open the image
		open(PATH + input_folder + files[i]);		
		
		// run morpholibj: boundaries ofa  labelled image
		run("Label Boundaries");		
		
		// remove boudnary from the segmentation
		selectWindow(files[i]);
		setThreshold(0, 0);
		//setThreshold(0, 0);
		run("Convert to Mask");		
		run("Invert");
		run("Grays");
		imageCalculator("Subtract create", files[i], image_name + "-bnd");
		selectWindow(files[i]);
		close();
		// convert into binary
		selectWindow("Result of " + files[i]);
		run("32-bit");
		run("Divide...", "value=255.000");
		run("8-bit");
		rename(files[i]);

		// convert boundaries into a mask with label 2
		selectWindow(image_name + "-bnd");		
		run("32-bit");
		run("Divide...", "value=255.000");
		run("Multiply...", "value=2.000");
		run("8-bit");
		// create the semantic mask
		imageCalculator("Add create", files[i], image_name + "-bnd");
		
		// save
		selectWindow("Result of " + files[i]);
		saveAs("Tiff", PATH + new_folder_seg+image_name+".tif");
		run("Close All");
	}
}