import { Component, OnInit } from '@angular/core';
import { Video } from '../../core/models/video.model';
import { VideoService } from '../../core/services/video.service';
import { StateService } from '../../shared/services/state.service';

@Component({
  selector: 'app-video-library',
  templateUrl: './video-library.component.html',
  styleUrls: ['./video-library.component.scss']
})
export class VideoLibraryComponent implements OnInit {
  videos: Video[] = [];
  selectedVideos: Video[] = [];

  constructor(
    private videoService: VideoService,
    private stateService: StateService
  ) { }

  ngOnInit(): void {
    this.loadVideos();
    this.stateService.selectedVideos$.subscribe(videos => {
      this.selectedVideos = videos;
    });
  }

  loadVideos(): void {
    this.videoService.listVideos().subscribe(videos => {
      this.videos = videos;
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      this.videoService.uploadVideo(file).subscribe(() => {
        this.loadVideos();
      });
    }
  }

  toggleVideoSelection(video: Video): void {
    if (this.isSelected(video)) {
      this.stateService.removeSelectedVideo(video);
    } else {
      this.stateService.addSelectedVideo(video);
    }
  }

  isSelected(video: Video): boolean {
    return this.selectedVideos.some(v => v.id === video.id);
  }

  deleteVideo(video: Video): void {
    this.videoService.deleteVideo(video.id).subscribe(() => {
      this.loadVideos();
      this.stateService.removeSelectedVideo(video);
    });
  }
}
