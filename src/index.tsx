import {
	definePlugin,
	PanelSection,
	PanelSectionRow,
	ServerAPI,
	quickAccessMenuClasses,
	Router,
	ToggleField,
} from "decky-frontend-lib";

import {
	VFC,
	useEffect,
	useState,
} from "react";

import { FaComment } from "react-icons/fa";

class DeckyDictationLogic {
	serverAPI: ServerAPI;
	pressedAt: number = Date.now();
	enabled: boolean = false;
	dictating = false;
	pushToDictate = false;

	constructor(serverAPI: ServerAPI) {
		this.serverAPI = serverAPI;
	}

	notify = async (message: string, duration: number = 1000, body: string = "") => {
		if (!body) {
			body = message;
		}
		this.serverAPI.toaster.toast({
			title: message,
			body: body,
			duration: duration,
			critical: true
		});
	}

	handleButtonInput = async (val: any[]) => {
		if (!this.enabled) {
			return;
		}
		if (this.pushToDictate) {
			this.handlePushToDictate(val);
		} else {
			this.handleToggleMode(val);
		}
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
	}

	handlePushToDictate = async (val: any[]) => {
		for (const inputs of val) {
			if (inputs.ulButtons && inputs.ulButtons & (1 << 15)) {
				if (!this.dictating) {
					this.dictating = true;
					this.serverAPI.callPluginMethod('begin', { push_to_dictate: true });
					this.notify("Decky Dictation", 2000, "Starting speech to text input");
				}
			} else if (this.dictating) {
				this.dictating = false;
				await this.serverAPI.callPluginMethod('end', {});
				this.notify("Decky Dictation", 2000, "Ending speech to text input");
			}
		}
	}

	handleToggleMode = async (val: any[]) => {
		for (const inputs of val) {
			if (Date.now() - this.pressedAt < 2000) {
				continue;
			}
			if (inputs.ulButtons && inputs.ulButtons & (1 << 15)) {
				this.pressedAt = Date.now();
				(Router as any).DisableHomeAndQuickAccessButtons();
				setTimeout(() => {
					(Router as any).EnableHomeAndQuickAccessButtons();
				}, 1000)
				this.serverAPI.callPluginMethod('begin', { push_to_dictate: false });
				await this.notify("Decky Dictation", 2000, "Starting speech to text input");
			}
			if (inputs.ulButtons && inputs.ulButtons & (1 << 16)) {
				this.pressedAt = Date.now();
				(Router as any).DisableHomeAndQuickAccessButtons();
				setTimeout(() => {
					(Router as any).EnableHomeAndQuickAccessButtons();
				}, 1000)
				this.serverAPI.callPluginMethod('end', {});
				await this.notify("Decky Dictation", 2000, "Ending speech to text input");
			}
		}
	}
}

const DeckyDictation: VFC<{ logic: DeckyDictationLogic }> = ({ logic }) => {
	const [enabled, setEnabled] = useState<boolean>(false);
	const [pushToDictate, setPushToDictate] = useState<boolean>(false);

	useEffect(() => {
		setEnabled(logic.enabled);
		setPushToDictate(logic.pushToDictate);
	}, []);

	return (
		<div>
			<PanelSection>
				<PanelSectionRow>
					<ToggleField
						label="Enable"
						checked={enabled}
						onChange={(e) => { setEnabled(e); logic.enabled = e; }}
					/>
				</PanelSectionRow>
				<PanelSectionRow>
					<ToggleField
						label="Push To Dictate"
						checked={pushToDictate}
						disabled={enabled}
						onChange={(e) => { setPushToDictate(e); logic.pushToDictate = e; }}
					/>
				</PanelSectionRow>
			</PanelSection>
			<PanelSection title="How to use:">
				<PanelSectionRow>
					<div>
						L5 to begin speech to text input, hold if "Push To Dictate" is enabled.
						<br />
						R5 to end speech to text input if "Push To Dictate" is disabled.
					</div>
					<div>
						Currently this plugin only works in a game (first opened game if you have more opened at once; not working in home, store or steam chat ui etc).
					</div>
				</PanelSectionRow>
			</PanelSection>
		</div>
	);
};


export default definePlugin((serverApi: ServerAPI) => {
	let logic = new DeckyDictationLogic(serverApi);
	let input_register = window.SteamClient.Input.RegisterForControllerStateChanges(logic.handleButtonInput);
	return {
		title: <div className={quickAccessMenuClasses.Title}>Decky Dictation</div>,
		content: <DeckyDictation logic={logic} />,
		icon: <FaComment />,
		onDismount() {
			input_register.unregister();
		},
		alwaysRender: true
	};
});
