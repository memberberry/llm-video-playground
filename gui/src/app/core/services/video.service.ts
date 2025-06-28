import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { Video } from '../models/video.model';

@Injectable({
  providedIn: 'root'
})
export class VideoService {

  constructor(private apiService: ApiService) { }

  uploadVideo(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    // Note: ApiService post method needs to be adjusted for FormData or a new method created
    // For now, directly use HttpClient for multipart/form-data
    return this.apiService['http'].post(`${this.apiService['baseUrl']}/videos/upload`, formData);
  }

  listVideos(): Observable<Video[]> {
    return this.apiService.get<Video[]>('videos/');
  }

  deleteVideo(videoId: number): Observable<any> {
    return this.apiService.delete(`videos/${videoId}`);
  }
}
