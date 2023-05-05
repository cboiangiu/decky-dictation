import {
	definePlugin,
	PanelSection,
	PanelSectionRow,
	ServerAPI,
	staticClasses,
	Router,
} from "decky-frontend-lib";

import {
	VFC,
} from "react";

import { FaComment } from "react-icons/fa";

class DeckyDictationLogic {
	serverAPI: ServerAPI;
	pressedAt: number = Date.now();

	constructor(serverAPI: ServerAPI) {
		this.serverAPI = serverAPI;
	}

	notify = async (message: string, duration: number = 1000, body: string = "") => {
		if (!body) {
			body = message;
		}
		await this.serverAPI.toaster.toast({
			title: message,
			body: body,
			duration: duration,
			critical: true
		});
	}

	handleButtonInput = async (val: any[]) => {
		/*
		R2 0
		L2 1
		R1 2
		R2 3
		Y  4
		B  5
		X  6
		A  7
		UP 8
		Right 9
		Left 10
		Down 11
		Select 12
		Steam 13
		Start 14
		QAM  ???
		L5 15
		R5 16*/
		for (const inputs of val) {
			if (Date.now() - this.pressedAt < 2000) {
				continue;
			}
			if (inputs.ulButtons && inputs.ulButtons & (1 << 13) && inputs.ulButtons & (1 << 5) && inputs.ulButtons & (1 << 1)) {
				this.pressedAt = Date.now();
				(Router as any).DisableHomeAndQuickAccessButtons();
				setTimeout(() => {
					(Router as any).EnableHomeAndQuickAccessButtons();
				}, 1000)
				await this.notify("Decky Dictation", 2000, "Starting speech to text input");
				await this.serverAPI.callPluginMethod('begin', {});
			}
			if (inputs.ulButtons && inputs.ulButtons & (1 << 13) && inputs.ulButtons & (1 << 5) && inputs.ulButtons & (1 << 0)) {
				this.pressedAt = Date.now();
				(Router as any).DisableHomeAndQuickAccessButtons();
				setTimeout(() => {
					(Router as any).EnableHomeAndQuickAccessButtons();
				}, 1000)
				await this.notify("Decky Dictation", 2000, "Ending speech to text input");
				await this.serverAPI.callPluginMethod('end', {});
			}
		}
	}

}

const DeckyDictation: VFC = () => {
	return (
		<PanelSection title="How to use:">
			<PanelSectionRow>
				<div>
					STEAM + B + L2 to begin speech to text input
					<br />
					STEAM + B + R2 to end speech to text input
				</div>
				<div>
					Currently this plugin only works in a game (first opened game if you have more opened at once; not working in home, store or steam chat ui etc).
				</div>
			</PanelSectionRow>
		</PanelSection>
	);

};


export default definePlugin((serverApi: ServerAPI) => {
	let logic = new DeckyDictationLogic(serverApi);
	let input_register = window.SteamClient.Input.RegisterForControllerStateChanges(logic.handleButtonInput);
	return {
		title: <div className={staticClasses.Title}>Decky Dictation</div>,
		content: <DeckyDictation />,
		icon: <FaComment />,
		onDismount() {
			input_register.unregister();
		},
		alwaysRender: true
	};
});