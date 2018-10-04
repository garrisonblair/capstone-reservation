import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal, Dropdown } from 'semantic-ui-react';
import axios from 'axios';

class ReservationDetailsModal extends Component {

  opened = false;
  state = {
    modalOpen: false,
    minHour: this.props.minHour || 8,
    maxHour: this.props.maxHour || 24,
    date: (new Date(this.props.date)).toDateString() || "please provide a date",
    defaultHour: this.props.defaultHour,
    defaultMinute: this.props.defaultMinute,
    roomNumber: this.props.roomNumber || "please provide a room number",
    hourOptions:[],
    minuteOptions: [
      { text: '00', value: 0 },
      { text: '10', value: 10 },
      { text: '20', value: 20 },
      { text: '30', value: 30 },
      { text: '40', value: 40 },
      { text: '50', value: 50 }
    ],
    reservedOptions: [
      // here the value should be 'this.props.username'
      { text: 'me', value: 1 }
    ]
  }

  generateHourOptions(minHour, maxHour) {
    let result = [];
    for (var i = minHour; i < maxHour; i++) {
      result.push({ text: i + '', value: i });
    }

    return result;
  }

  componentWillMount() {
    this.setState({
      hourOptions: this.generateHourOptions(this.state.minHour, this.state.maxHour)
    })
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
              <Header>Room {this.state.roomNumber} </Header>
              <p>Date: {this.state.date}</p>
              <br />
              <span>
                <span className="inputLabel">From:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.state.hourOptions} defaultValue={this.state.defaultHour} />
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.state.minuteOptions} defaultValue={this.state.defaultMinute} />
                <span className="inputLabel" id="toLabel">To:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.state.hourOptions} />
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.state.minuteOptions} />
              </span>
              <br /><br />
              <span>
                <span className="inputLabel">Reserved by:</span>
                <Dropdown compact placeholder='hh' selection options={this.state.reservedOptions} defaultValue={this.state.reservedOptions[0].value} />
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
