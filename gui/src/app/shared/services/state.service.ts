import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Video } from '../../core/models/video.model';

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private selectedVideosSubject = new BehaviorSubject<Video[]>([]);
  selectedVideos$: Observable<Video[]> = this.selectedVideosSubject.asObservable();

  constructor() { }

  addSelectedVideo(video: Video): void {
    const currentVideos = this.selectedVideosSubject.value;
    if (!currentVideos.some(v => v.id === video.id)) {
      this.selectedVideosSubject.next([...currentVideos, video]);
    }
  }

  removeSelectedVideo(video: Video): void {
    const currentVideos = this.selectedVideosSubject.value;
    this.selectedVideosSubject.next(currentVideos.filter(v => v.id !== video.id));
  }

  clearSelectedVideos(): void {
    this.selectedVideosSubject.next([]);
  }

  private refreshHistorySubject = new BehaviorSubject<void>(undefined);
  refreshHistory$: Observable<void> = this.refreshHistorySubject.asObservable();

  triggerHistoryRefresh(): void {
    this.refreshHistorySubject.next();
  }
}
