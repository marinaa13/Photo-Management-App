
>Tema IAp1 - Simion Marina, grupa 311CA

 This is a simple photo management web application built with Flask. The application allows an administrator to upload and manage photos, which are then displayed in a public gallery. 
 
 ## Features 
**Public Photo Gallery**: Displays all uploaded photos categorized by their respective categories. 
**Admin Authentication**: Only authenticated users can upload or delete photos. 
**Photo Upload**: Authenticated users can upload photos with a specified name and category using a dropdown menu for the category selection. 
**Thumbnail Generation**: Automatically generates a low-resolution thumbnail for each uploaded photo. 
**Photo Deletion**: Authenticated users can delete photos from the gallery.
**About Page**: Static page with information about the application or user.

## Docker setup
To containerize the application using Docker, follow these steps:
1. **Build the Docker Image**: `bash docker build -t photo-management-app . `
2. **Run the Docker Container**: `bash docker run -p 5000:5000 -it photo-management-app `
	 The application will be accessible at `http://localhost:5000`.

## Usage 
 **Admin Login:** 
	  Username: `admin` 
	  Password: `123456`

## Uploading Photos
1. Log in as an admin.
2. Navigate to the upload page. 
3.  Select an image file, provide a name, and choose a category from the dropdown menu. 
4. Submit the form to upload the photo.

## Deleting Photos
1. Log in as an admin.
2. Navigate to the gallery.
3. Click the delete button below the photo you want to remove.

## Notes 
1. Ensure that the `uploads` and `thumbnails` directories exist within the `static` directory. The application will create them if they don't exist. 
2. The thumbnails are generated with a Gaussian blur to create low-resolution versions of the uploaded images. 
3. The categories are managed using a dropdown menu for better user experience.
4.  The photos are grouped up by category.
5. The archive also contains a folder *photos_to_upload*, from where the user can select some flowers based on their season to upload to the gallery :)