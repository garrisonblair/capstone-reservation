import React, { Component } from 'react';
import settings from '../../config/settings';
import './ReservationDetailsModal.scss';
import { Button, Header, Modal, Dropdown, Button } from 'semantic-ui-react'

class ReservationDetailsModal extends Component {
  componentDidMount() {
    console.log(settings)
  }

  hourOptions = [
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
    { text: '23', value: 23 },
    { text: '24', value: 24 }
  ]

  minuteOptions = [
    { text: '00', value: 0 },
    { text: '10', value: 10 },
    { text: '20', value: 20 },
    { text: '30', value: 30 },
    { text: '40', value: 40 },
    { text: '50', value: 50 }
  ]

  reservedOptions = [
    { text: 'me' }
  ]

  render() {
    return (
      <div id="reservation-details-modal">
        <Modal trigger={<Button>Show Modal</Button>} centered={false}>
          <Modal.Header>Reservation Details</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              <Header>Room #</Header>
              <p>Date: </p>
              <br/>
              <span>
                <span class="inputLabel">From:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.hourOptions} />
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.minuteOptions} />
                <span class="inputLabel" id="toLabel">To:</span>
                <Dropdown placeholder='hh' selection compact className="timeSelection" options={this.hourOptions} />
                <Dropdown placeholder='mm' selection compact className="timeSelection" options={this.minuteOptions} />
              </span>
              <br/><br/>
              <span>
                <span class="inputLabel">Reserved by:</span>
                <Dropdown compact placeholder='hh' selection options={this.reservedOptions} />
              </span>
              
            </Modal.Description>
          </Modal.Content>
        </Modal>
      </div>
    )
  }
}

export default ReservationDetailsModal;
