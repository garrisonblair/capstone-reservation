import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal, Dropdown } from 'semantic-ui-react';
import axios from 'axios';

class ReservationDetailsModal extends Component {

  roomNumber = this.props.roomNumber;
  date = this.props.date;
  defaultHour = this.props.defaultHour;
  defaultMinute = this.props.defaultMinute;
  opened = false;
  hourOptions = this.props.hourOptions;
  state = { modalOpen: false }

  minuteOptions = [
    { text: '00', value: 0 },
    { text: '10', value: 10 },
    { text: '20', value: 20 },
    { text: '30', value: 30 },
    { text: '40', value: 40 },
    { text: '50', value: 50 }
  ];

  reservedOptions = [
    // here the value should be 'this.props.username'
    { text: 'me', value: 1 }
  ]
  // setHourOptions(startHour, endHour) {
  //   for (var i = startHour; i < endHour; i++) {
  //     this.hourOptions.push({text: i + '', value: i});
  //     console.log(i);
  //   }
  // }

  //This is a setup for me
  testSetup() {
    this.roomNumber = 23;
    this.defaultHour = 8;
    this.defaultMinute = 50;
    this.date = new Date().toDateString();
    this.hourOptions = [
      { text: '08', value: 8 },
      { text: '09', value: 9 },
      { text: '10', value: 10 },
      { text: '11', value: 11 },
      { text: '12', value: 12 },
      { text: '13', value: 13 },
      { text: '14', value: 14 },
      { text: '15', value: 15 },
      { text: '16', value: 16 },
      { text: '17', value: 17 },
      { text: '18', value: 18 },
      { text: '19', value: 19 },
      { text: '20', value: 20 },
      { text: '21', value: 21 },
      { text: '22', value: 22 },
      { text: '23', value: 23 }
    ];

  }
  componentWillMount() {
    this.testSetup();
  }

  closeModal = () => this.setState({ modalOpen: false });
  handleOpen = () => this.setState({ modalOpen: true });
  handleReserve() {
    axios.get(`${settings.API_ROOT}/users`).then(response => console.log(response.data[0]));
  }

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal trigger={<div onClick={this.handleOpen}>Click me</div>} centered={false} size={"tiny"} open={this.state.modalOpen}>
          <Modal.Header>Reservation Details</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              <Header>Room # {this.roomNumber}</Header>
              <p>Date: {this.date} </p>
              <br />
              <span>
                <span className="inputLabel">From:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.hourOptions} defaultValue={this.defaultHour}/>
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.minuteOptions} defaultValue={this.defaultMinute} />
                <span className="inputLabel" id="toLabel">To:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.hourOptions} />
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.minuteOptions} />
              </span>
              <br /><br />
              <span>
                <span className="inputLabel">Reserved by:</span>
                <Dropdown compact placeholder='hh' selection options={this.reservedOptions} defaultValue={this.reservedOptions[0].value} />
              </span>
              <br /><br />
              <div>
                <Button content='Reserve' primary onClick={this.handleReserve} />
                <Button content='Cancel' secondary onClick={this.closeModal} />
              </div>
            </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )
  }
}

export default ReservationDetailsModal;
