import React from 'react';
import renderer from 'react-test-renderer';
import Registration from '../../components/Registration/index';

it('Show registration', () => {
    const tree = renderer
        .create(<Registration></Registration>)
        .toJSON();
    expect(tree).toMatchSnapshot();
});
