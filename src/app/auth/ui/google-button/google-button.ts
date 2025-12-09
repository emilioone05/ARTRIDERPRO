import { Component, output } from '@angular/core';

@Component({
  selector: 'app-google-button',
  imports: [],
  templateUrl: './google-button.html',
})
export class GoogleButton {
  onClick= output<void>();
}
