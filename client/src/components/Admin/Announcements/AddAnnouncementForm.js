import React, { Component } from 'react';
import { Form, TextArea, Button } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';
import './AddAnnouncementForm.scss';

class AddAnnouncementForm extends Component {
  state = {
    // text: '',
    // fromDate: '',
    // toDate: '',
  }

  handleAddButton = () => {

  }

  handleTextOnChange = () => {

  }

  handleFromDateOnChange = () => {

  }

  handleToDateOnChange = () => {

  }

  render() {
    return (
      <div id="add-announcement-form">
        <Form>
          <TextArea placeholder="Write announcement here" />
        </Form>
        <div className="grid-container">
          <div className="from-date">
            From:
            <input type="date" />
          </div>
          <div className="to-date">
            To:
            <input type="date" />
          </div>
          <Button className="add-button">Add</Button>
        </div>
      </div>
    );
  }
}

export default AddAnnouncementForm;
