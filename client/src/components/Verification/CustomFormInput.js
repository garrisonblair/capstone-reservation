import React, {Component} from 'react';
import {Loader, Form, Input, Button, Icon, Step, Label} from 'semantic-ui-react';


class CustomFormInput extends Component {
    componentDidMount() {
      console.log(this.props)
    }

    renderErrorMessage() {
      let component = '';
      if (this.props.errormessage) {
        component = (
          <div>
            <Label color="red" pointing='below'>
              {this.props.errormessage}
            </Label>
          </div>
        )
      }
      return component;
    }

    render() {
      return (
        <Form.Field>
          <label>Student ID:</label>
          {this.renderErrorMessage()}
          <Input
            {...this.props}
          />
        </Form.Field>
      )
    }
}

export default CustomFormInput;
