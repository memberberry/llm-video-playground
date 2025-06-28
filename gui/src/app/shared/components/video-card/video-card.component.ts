import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Video } from '../../../core/models/video.model';

@Component({
  selector: 'app-video-card',
  templateUrl: './video-card.component.html',
  styleUrls: ['./video-card.component.scss']
})
export class VideoCardComponent {
  @Input() video!: Video;
  @Output() delete = new EventEmitter<void>();

  onDelete(event: MouseEvent): void {
    event.stopPropagation();
    this.delete.emit();
  }
}
