import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalysisInterfaceComponent } from './analysis-interface.component';

describe('AnalysisInterfaceComponent', () => {
  let component: AnalysisInterfaceComponent;
  let fixture: ComponentFixture<AnalysisInterfaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AnalysisInterfaceComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AnalysisInterfaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
