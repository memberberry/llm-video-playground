import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from './shared/components/header/header.component';
import { HistoryCardComponent } from './shared/components/history-card/history-card.component';
import { VideoCardComponent } from './shared/components/video-card/video-card.component';
import { VideoLibraryComponent } from './components/video-library/video-library.component';
import { HistoryTimelineComponent } from './components/history-timeline/history-timeline.component';
import { AnalysisInterfaceComponent } from './components/analysis-interface/analysis-interface.component';
import { HistoryDetailDialogComponent } from './shared/components/history-detail-dialog/history-detail-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HistoryCardComponent,
    VideoCardComponent,
    VideoLibraryComponent,
    HistoryTimelineComponent,
    AnalysisInterfaceComponent,
    HistoryDetailDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
