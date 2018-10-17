import axios from 'axios';
import React, {Component} from 'react';
import settings from '../../config/settings';
import './Registration.scss';
import SweetAlert from 'sweetalert2-react';
import {Form, Input, Button, Icon, Step, Loader} from 'semantic-ui-react';

class Registration extends Component {

  state = {
    encsUsername: '',
    showModal: false,
    modalTitle: '',
    modalText: '',
    modalType: 'info',
    showLoader: false
  }

  componentWillMount(){
    //This is only for testing.
    if(this.props.showLoaderForTest){
      this.setState({showLoader:true});
    }
  }

  handleEncsUsername = (event) => {
    this.setState({encsUsername: event.target.value});
  }

  closeModal = () => {
    this.setState({showModal: false})
    if (this.state.modalType === 'success') {
      this.props.history.push('/login');
    }

  }

  sendEmail = () => {
    this.setState({showLoader: true})
    const data = {"username": `${this.state.encsUsername}`};
    console.log(data);
    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/register`,
      data: data
    })
      .then((response) => {
        if (response.status == 201) {
          this.setState({
            showLoader: false,
            showModal: true,
            modalTitle: 'Succeed',
            modalText: 'A verification message has been send to your ENCS email.',
            modalType: 'success',
          })
        }

      })
      .catch((error) => {
        this.setState({showLoader: false})
        if (error.message.includes('302')) {
          this.setState({
            showModal: true,
            modalTitle: 'Warning',
            modalText: 'You have already sent a verification to your ENCS email.',
            modalType: 'warning',
          })
        }
        else if (error.message.includes('400')) {
          this.setState({
            showModal: true,
            modalTitle: 'Error',
            modalText: "We couldn't find this user in the system.",
            modalType: 'error',
          })
        }
      })
  }

  renderLoader() {
    return (
      <div>
        <Loader active inline='centered' size="large" />
      </div>
    )
  }

  renderMainForm() {
    return (
      <div>
        <h1>Registration</h1>
        <Step.Group size="mini" widths={2}>
          <Step active>
            <Icon name="envelope" />
            <Step.Content>
              <Step.Title>Step 1</Step.Title>
              <Step.Description>ENCS username verification</Step.Description>
            </Step.Content>
          </Step>
          <Step>
            <Icon name="cog" />
            <Step.Content>
              <Step.Title>Step 2</Step.Title>
              <Step.Description>Account setup</Step.Description>
            </Step.Content>
          </Step>
        </Step.Group>
        <p>Please enter your ENCS username. A validation will be sent to your ENCS email.</p>
        <Form.Field>
          <Input
            fluid
            size='small'
            icon='user'
            iconPosition='left'
            placeholder='ex. a_test'
            onChange={this.handleEncsUsername}
          />
        </Form.Field>
        <Form.Field>
          <br />
          <Button fluid size='small' icon onClick={this.sendEmail}>
            Send Email
      </Button>
        </Form.Field>
      </div>
    )
  }

  render() {
    return (
      <div id="registration">
        <div className="container">
          {this.state.showLoader ? this.renderLoader() : this.renderMainForm()}
        </div>
        <SweetAlert
          show={this.state.showModal}
          title={this.state.modalTitle}
          text={this.state.modalText}
          type={this.state.modalType}
          onConfirm={this.closeModal}
        />
      </div>
    )
  }
}

export default Registration;
