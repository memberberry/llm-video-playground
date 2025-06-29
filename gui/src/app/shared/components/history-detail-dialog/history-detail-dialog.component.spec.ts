import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoryDetailDialogComponent } from './history-detail-dialog.component';

describe('HistoryDetailDialogComponent', () => {
  let component: HistoryDetailDialogComponent;
  let fixture: ComponentFixture<HistoryDetailDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HistoryDetailDialogComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HistoryDetailDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
