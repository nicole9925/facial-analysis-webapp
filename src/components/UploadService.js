class UploadService {
  async UploadToServer(img, name) {

    const data = new FormData();

    const parts = img[0].split(';')

    data.append('file', parts[2].split(",")[1]);
    data.append('filename', name);
    
    let response = await fetch('/api/upload/', {
      method: 'POST',
      body: data
    })
    let resp_data = await response.json()
    return resp_data



  }
 
  // getImages() {
  //   return http.get("/img");
  // }
}

export default new UploadService();