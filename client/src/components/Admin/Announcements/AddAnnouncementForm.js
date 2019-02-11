import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Form, TextArea, Button, Input,
} from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './AddAnnouncementForm.scss';

class AddAnnouncementForm extends Component {
  state = {
    subject: '',
    text: '',
    fromDate: '',
    toDate: '',
  }

  handleSubjectOnChange = (e, data) => { this.setState({ subject: data.value }); }

  handleTextOnChange = (e, data) => { this.setState({ text: data.value }); }

  handleFromDateOnChange = (e, data) => { this.setState({ fromDate: data.value }); }

  handleToDateOnChange = (e, data) => { this.setState({ toDate: data.value }); }

  handleAddButton = () => {
    const {
      subject, text, fromDate, toDate,
    } = this.state;
    const { syncFunction } = this.props;
    console.log(subject);
    console.log(text);
    console.log(fromDate);
    console.log(toDate);
    api.createAnnouncement(subject, text, fromDate, toDate)
      .then((r) => {
        if (r.status === 201) {
          syncFunction();
        }
        console.log(r);
      });
  }

  render() {
    return (
      <div id="add-announcement-form">
        <Form>
          <Input placeholder="Subject" className="subject-input" />
          <TextArea placeholder="Write announcement here" onChange={this.handleTextOnChange} />
        </Form>
        <div className="grid-container">
          <div className="from-date">
            From:
            <Input type="date" onChange={this.handleFromDateOnChange} size="small" />
          </div>
          <div className="to-date">
            To:
            <Input type="date" onChange={this.handleToDateOnChange} size="small" />
          </div>
          <Button className="add-button" onClick={this.handleAddButton}>Add</Button>
        </div>
      </div>
    );
  }
}

AddAnnouncementForm.propTypes = {
  syncFunction: PropTypes.func.isRequired,
};

export default AddAnnouncementForm;
