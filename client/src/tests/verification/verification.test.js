import React from 'react';
import renderer from 'react-test-renderer';
import Verification from '../../components/Verification/index';

it('Show registration', () => {
    const tree = renderer
        .create(<Verification match={{params: {token: 1}}}></Verification>)
        .toJSON();
    expect(tree).toMatchSnapshot();
});

it('Show registration form', () => {
    const tree = renderer
        .create(<Verification match={{params: {token: 1}}} showFormForTesting={true}></Verification>)
        .toJSON();
    expect(tree).toMatchSnapshot();
});
