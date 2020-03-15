import { Component, OnInit } from '@angular/core';
import { DataService } from './_services/data.service';
import { News } from './_models/news';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit  {
  title = 'corona-live';
  news: News[] = []

  constructor (private dataService: DataService) {}

  ngOnInit() {
    // this.getNews();
  }

  getNews(): void {
    this.dataService.getNews().subscribe(result => {
      this.news = result;
    }, error => {
      console.log("ERROR - connection problem");
      // alert("К сожалению, произошли проблемы при подключении к серверу, попробуйте позже");
    });
  }


}
