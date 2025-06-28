import { Component, Input } from '@angular/core';
import { History } from '../../../core/models/history.model';

@Component({
  selector: 'app-history-card',
  templateUrl: './history-card.component.html',
  styleUrls: ['./history-card.component.scss']
})
export class HistoryCardComponent {
  @Input() historyItem!: History;
}
